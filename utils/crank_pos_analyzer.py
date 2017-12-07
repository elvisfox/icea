
import math

from utils.pulse_counter import pulse_counter

class crank_pos_analyzer:
	def __init__(self, crank_pc, cam_pcs, pulses_per_cyl, skipped_pulses, TDC_pulse, firing_order):
		# configuration
		self.crank_pc = crank_pc
		self.cam_pcs = cam_pcs
		self.pulses_per_cyl = pulses_per_cyl
		self.skipped_pulses = skipped_pulses
		self.TDC_pulse = TDC_pulse
		self.firing_order = firing_order
		self.no_of_cyl = len(firing_order)

		# state
		self.in_sync = False
		self.pulse_width = math.inf
		self.prev_TDC_time = 0
		self.rpm = 0

	# process states from CSV dictionary
	# return True if TDC is detected
	def sample(self, line):							# TODO: identify cylinders, check firing order, calculate cam advance
		# run pulse counters
		crank_pulse = self.crank_pc.sample(line)
		for cam in self.cam_pcs:
			cam.sample(line)		# TODO: Store cam pulse positions

		# proceed only if crank pulse detected
		if not crank_pulse:
			return False

		# check pulse width
		long_pulse_th = self.pulse_width * (1 + self.skipped_pulses/2.0)
		if self.crank_pc.period > long_pulse_th:
			# long pulse detected, check pulse counter
			if self.in_sync and self.crank_pc.counter != self.pulses_per_cyl:
				self.in_sync = False
				print('Warning! Crank out of sync at t=' + str(self.crank_pc.became_act))
				#raise Exception('Crank out of sync')
			else:
				#print('Fuck yea, long pulse')
				
				# reset Crank counter
				self.crank_pc.reset()

				# in sync now
				self.in_sync = True

		else:
			# store pulse width
			self.pulse_width = self.crank_pc.period

			# regular pulse, check for TDC
			if self.in_sync and self.crank_pc.counter == self.TDC_pulse - 1:
				# TDC detected, reset cams
				for cam in self.cam_pcs:
					cam.reset()

				# calculate rpm
				self.rpm = 60e3 / ((self.crank_pc.became_act - self.prev_TDC_time) * self.no_of_cyl / 2)

				# store TDC time
				self.prev_TDC_time = self.crank_pc.became_act

				return True

		# not a TDC
		return False
