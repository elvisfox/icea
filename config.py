
from utils.converters import *

# output file
output_file = 'ololo.csv'

# this also sets number of cylinders
# ( cylinder, [ cam pulses ] )
firing_order = [
	( 1, [2, 1, 1, 0] ),
	( 2, [2, 0, 0, 1] ),
	( 3, [0, 1, 1, 0] ),
	( 4, [1, 2, 0, 1] ),
	( 5, [0, 2, 1, 0] ),
	( 6, [1, 0, 0, 1] ),
]

# crankshaft position sensor
crank_channel 			= 'D1'			# scope channel
crank_polarity 			= 1				# active level
crank_pulses_per_cyl 	= 10			# how many pulses does CKP produce per one cylinder stroke?
crank_skipped_pulses	= 2				# how many pulses are skipped in between?
crank_TDC_pulse			= 8				# pulse number where TDC position is located

# list of camshaft channels
#	cam name :			(src name, polarity, angle)
cam_channels = {
	'In B1':			('D2',	0,	40),
	'In B2':			('D3',	0,	40),
	'Ex B1':			('D4',	0,	40),
	'Ex B2':			('D5',	0,	40),
}

# glitch filter (how many samples can be considered as a glitch?)
# this also enables median filter for analog signals
glitch_filter = 2

# dict of analog channels
#    tgt name : 		(src name, 		converter,		units),
analog_channels = {
	'APP S1':			('Channel A', 	passthru,		None ),
	'TPS S1 B1':		('Channel B', 	passthru,		None ),
}

