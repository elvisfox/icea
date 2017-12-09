import sys

from config import *
from utils.csv_reader import csv_reader
from utils.csv_writer import csv_writer
from utils.pulse_counter import pulse_counter
from utils.analog_average import analog_average
from utils.crank_pos_analyzer import crank_pos_analyzer

# open input file
try:
	csv_rdr = csv_reader(sys.argv[1])
except:
	print('Failed to open input file.')
	sys.exit(1)

# find the time unit
time_unit_str = csv_rdr.unit_dict['Time']
if time_unit_str == 's':
	time_unit = 1.0
elif time_unit_str == 'ms':
	time_unit = 1e-3
elif time_unit_str == 'us':
	time_unit = 1e-6
else:
	print('Unknown time unit: ' + time_unit_str)
	sys.exit(1)

# init pulse counters for crankshaft and camshafts
crank_pc = pulse_counter(crank_polarity, crank_channel, glitch_filter)
cam_pcs = list()
for cam in cam_channels:
	cam_pcs.append(pulse_counter(cam_polarity, cam, glitch_filter))

# init crankshaft position analyzer
crank_pos = crank_pos_analyzer(crank_pc, cam_pcs, crank_pulses_per_cyl, crank_skipped_pulses, crank_TDC_pulse,
								firing_order, time_unit)

# read until first active edge of crank
first = False
while not first:
	line = csv_rdr.readline()
	first = crank_pc.sample(line)
	for cam in cam_pcs:
		cam.sample(line)

print('First edge found at time ' + str(crank_pc.became_act))

# read until first TDC
first = False
while not first:
	line = csv_rdr.readline()
	first = crank_pos.sample(line)

print('First TDC found at time ' + str(crank_pos.prev_TDC_time))

# prepare dict of output fields : units
out_dict = { 
	'Time' : time_unit_str, 
	'RPM' : None,
	'cyl' : None,
}

# init analog channels
med_filt = ((glitch_filter + 1) // 2) * 2 + 1		# 0 -> 1, 1 -> 3, 2 -> 3, 3 -> 5, 4 -> 5, ...
ana_avg = dict()
for ch, cfg in analog_channels.items():
	# specified units?
	unit = cfg[2]
	if unit == None:
		# not specified, use input units
		unit = csv_rdr.unit_dict[cfg[0]]
	# add channel target name to output list
	out_dict[ch] = unit
	# create averager for each analog channel
	ana_avg[ch] = analog_average(med_filt)

# open output file
csv_out = csv_writer(output_file, out_dict)

# process data
try:
	while True:
		# read new line, break if EOF
		line = csv_rdr.readline()
		if line == None:
			break

		# sample analog channels
		for ch, cfg in analog_channels.items():
			# use converter
			smpl = cfg[1]( line[ cfg[0] ] )
			# sample
			ana_avg[ch].sample(smpl)

		# process sample in Crank Pos Analyzer
		is_tdc = crank_pos.sample(line)

		# skip until TDC is detected
		if not is_tdc:
			continue

		# prepare output data
		csv_out.values['Time'] = line['Time']
		csv_out.values['RPM'] = crank_pos.rpm
		csv_out.values['cyl'] = crank_pos.cylinder

		# prepare analog channels
		for ch in analog_channels:
			csv_out.values[ch] = ana_avg[ch].result()

		# write to output file
		csv_out.store()
		sys.stdout.write('Processing time ' + str(line['Time']) + ' ' + time_unit_str + '      \r')

	# finalize stuff
	print('\nSuccess')

except KeyboardInterrupt:
	print('\nInterrupted by user')

