
class analog_average:

	def reset(self):
		self.sum = 0
		self.count = 0

	def __init__(self):
		self.reset()

	def sample(self, value):
		self.sum += value
		self.count += 1

	def result(self):
		# calculate averaged value
		val = self.sum / self.count

		# reset sum & counter
		self.reset()

		# return value
		return val
