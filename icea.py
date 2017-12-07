import sys

from config import *
from utils.csv_reader import csv_reader
from utils.csv_writer import csv_writer
from utils.pulse_counter import pulse_counter
from utils.crank_pos_analyzer import crank_pos_analyzer

# open input file
try:
	csv_rdr = csv_reader(sys.argv[1])
except:
	print('Failed to open input file.\n')
	sys.exit(1)

# init pulse counters for crankshaft and camshafts
crank_pc = pulse_counter(crank_polarity, crank_channel)
cam_pcs = list()
for cam in cam_channels:
	cam_pcs.append(pulse_counter(cam_polarity, cam))

# init crankshaft position analyzer
crank_pos = crank_pos_analyzer(crank_pc, cam_pcs, crank_pulses_per_cyl, crank_skipped_pulses, crank_TDC_pulse,
								firing_order)

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

# TODO: prepare list of output fields
out_list = ['Time', 'RPM']

# open output file
csv_out = csv_writer(output_file, out_list)

# process data
while True:
	# read new line, break if EOF
	line = csv_rdr.readline()
	if line == None:
		break

	# process sample in Crank Pos Analyzer
	is_tdc = crank_pos.sample(line)

	# skip until TDC is detected
	if not is_tdc:
		continue

	# prepare output data
	csv_out.values['Time'] = line['Time']
	csv_out.values['RPM'] = crank_pos.rpm

	# write to output file
	csv_out.store()
	print('TDC found: RPM = ' + str(crank_pos.rpm))

# finalize stuff
print('Success')
