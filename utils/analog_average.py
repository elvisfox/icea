

# receives a list of samples
def median(input):
	# sort samples
	input_sorted = sorted(input)

	# choose median sample
	sample_index = len(input_sorted) // 2	# no +1 because indices are 0-based

	# return it
	return input_sorted[sample_index]


class analog_average:

	def reset(self):
		self.median_queue = []
		self.sum = 0
		self.count = 0

	def __init__(self, median_filter):
		# configuration
		self.median_filter = median_filter

		# state
		self.reset()

	def sample(self, value):
		# put sample into median queue
		self.median_queue.append(value)

		# remove old samples from queue
		while len(self.median_queue) > self.median_filter:
			del self.median_queue[0]
		else:
			# check if queue is long enough
			if len(self.median_queue) < self.median_filter:
				return

		# increment sample counter and store filtered sample
		self.count += 1
		self.sum += median(self.median_queue)

	def result(self):
		# calculate averaged value
		val = self.sum / self.count

		# reset sum & counter
		self.reset()

		# return value
		return val
