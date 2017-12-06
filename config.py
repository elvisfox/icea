

# this also sets number of cylinders
firing_order = [ 1, 2, 3, 4, 5, 6 ]

# crankshaft position sensor
crank_channel 			= 'D0'			# scope channel
crank_polarity 			= 1				# active level
crank_pulses_per_cyl 	= 10			# how many pulses does CKP produce per one cylinder stroke?
crank_skipped_pulses	= 2				# how many pulses are skipped in between?
crank_TDC_pulse			= 8				# pulse number where TDC position is located

# list of camshaft channels
cam_channels 			= ['D1']
cam_polarity 			= 0
