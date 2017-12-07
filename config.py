
from utils.converters import *

# output file
output_file = 'ololo.csv'

# this also sets number of cylinders
# ( cylinder, [ cam pulses ] )
firing_order = [
	( 1, [2, 1] ),
	( 2, [2, 0] ),
	( 3, [0, 1] ),
	( 4, [1, 2] ),
	( 5, [0, 2] ),
	( 6, [1, 0] ),
]

# crankshaft position sensor
crank_channel 			= 'D0'			# scope channel
crank_polarity 			= 1				# active level
crank_pulses_per_cyl 	= 10			# how many pulses does CKP produce per one cylinder stroke?
crank_skipped_pulses	= 2				# how many pulses are skipped in between?
crank_TDC_pulse			= 8				# pulse number where TDC position is located

# list of camshaft channels
cam_channels 			= ['D1', 'D1']
cam_polarity 			= 0

# dict of analog channels
#    tgt name : 		(src name, 		converter,		units),
analog_channels = {
	'TPS S1 B1':		('Channel A', 	passthru,		None ),
}
