
class pulse_counter:

	def __init__(self, active_level, channel, glitch_filter):
		# configuration
		self.active_level = active_level
		self.state = active_level			# prevent detection of active edge at a very first sample
		self.channel = channel
		self.glitch_filter = glitch_filter

		# state
		self.became_act = 0
		self.became_pasv = 0
		self.period = 0
		self.duty = 0
		self.counter = 0
		self.glitch_counter = 0
		self.glitch_time = 0

	# process state from CSV dictionary
	# return True if active edge is detected
	def sample(self, line):
		# read new state
		new_state = bool(line[self.channel])

		# proceed only if state changed
		if new_state == self.state:
			# reset glitch counter (could be previously modified)
			self.glitch_counter = 0
			# return, nothing happened
			return False

		#print('State changed! Now ' + str(new_state))

		# *** glitch filter ***

		# store time when signal actually changed state
		if self.glitch_counter == 0:
			self.glitch_time = line['Time'];

		# increment counter
		self.glitch_counter += 1

		# check counter target
		if self.glitch_counter <= self.glitch_filter:
			return False

		# ok, glitch filter passed, reset counter
		self.glitch_counter = 0
		
		# *** end of glitch filter ***

		# store new state
		self.state = new_state

		# which level?
		if new_state == self.active_level:
			# active level, calculate period
			self.period = self.glitch_time - self.became_act

			# calculate duty
			self.duty = (self.became_pasv - self.became_act) / self.period

			# store time
			self.became_act = self.glitch_time

			# increment counter
			self.counter += 1

			#print('Period: ' + str(self.period) + ', Duty: ' + str(self.duty))
			return True

		else:
			# passive level, store time
			self.became_pasv = self.glitch_time

		return False

	def reset(self):
		self.counter = 0
