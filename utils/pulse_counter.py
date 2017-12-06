
class pulse_counter:

	def __init__(self, active_level, channel):
		self.active_level = active_level
		self.state = active_level			# prevent detection of active edge at a very first sample
		self.channel = channel
		self.became_act = 0
		self.became_pasv = 0
		self.period = 0
		self.duty = 0
		self.counter = 0

	# read and process state from CSV dictionary
	# returns True if active edge is detected
	def sample(self, dict):
		# read new state
		new_state = bool(dict[self.channel])

		# proceed only if state changed
		if new_state == self.state:
			return False

		#print('State changed! Now ' + str(new_state))

		# read current time from dict
		cur_time = dict['Time']

		# store new state
		self.state = new_state

		# which level?
		if new_state == self.active_level:
			# active level, calculate period
			self.period = cur_time - self.became_act

			# calculate duty
			self.duty = (self.became_pasv - self.became_act) / self.period

			# store time
			self.became_act = cur_time

			# increment counter
			self.counter += 1

			#print('Period: ' + str(self.period) + ', Duty: ' + str(self.duty))
			return True

		else:
			# passive level, store time
			self.became_pasv = cur_time

		return False

	def reset(self):
		self.counter = 0
