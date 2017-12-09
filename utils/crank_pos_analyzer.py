
import math
#from itertools import cycle

from utils.pulse_counter import pulse_counter

def calc_angle(t, t1, a1, t2, a2):
	# ensure a2 > a1
	if a2 < a1:
		a2 += 720

	# calculate angle by proportion
	a = a1 + (a2 - a1) * (t - t1) / (t2 - t1)

	# return
	#print(str(t) + ' ' + str(t1) + ' ' + str(a1) + ' ' + str(t2) + ' ' + str(a2) + ' ' + str(a))
	return a % 720

class crank_pos_analyzer:
	def unsync(self):
		self.in_sync = False
		self.pulse_width = math.inf
		self.cylinder = 0
		self.expect_cyl = 0

	def __init__(self, crank_pc, cam_pcs, pulses_per_cyl, skipped_pulses, TDC_pulse, firing_order,
				time_unit, cam_offsets, mon_pcs, mon_offsets):
		# configuration
		self.crank_pc = crank_pc
		self.cam_pcs = cam_pcs
		self.pulses_per_cyl = pulses_per_cyl
		self.skipped_pulses = skipped_pulses
		self.TDC_pulse = TDC_pulse
		self.firing_order = firing_order
		self.no_of_cyl = len(firing_order)
		self.time_unit = time_unit
		self.cam_offsets = cam_offsets
		self.mon_pcs = mon_pcs
		self.mon_offsets = mon_offsets

		# state
		self.unsync()
		self.prev_TDC_time = 0
		self.rpm = 0
		self.prev_angle = 0
		self.cam_time = [-math.inf] * len(cam_pcs)
		self.cam_angles = [0] * len(cam_pcs)
		self.mon_time = [-math.inf] * len(mon_pcs)
		self.mon_adv = [0] * len(mon_pcs)

	# process states from CSV dictionary
	# return True if TDC is detected
	def sample(self, line):
		# run pulse counters
		crank_pulse = self.crank_pc.sample(line)
		for i, cam in enumerate(self.cam_pcs):
			if cam.sample(line) and cam.counter == 1:
				self.cam_time[i] = cam.became_act 	# store cam timings
		for i, mon in enumerate(self.mon_pcs):
			if mon.sample(line):
				if mon.counter > 1:
					print('Warning! Advance monitor ' + str(i) + ' got extra pulse at t=' + str(mon.became_act))
				self.mon_time[i] = mon.became_act 	# store cam timings

		# proceed only if crank pulse detected
		if not crank_pulse:
			return False

		# ***    ok, pulse detected    ***

		# check pulse width
		long_pulse_th = self.pulse_width * (1 + self.skipped_pulses/2.0)
		if self.crank_pc.period > long_pulse_th:
			# long pulse detected, check pulse counter
			if self.in_sync and self.crank_pc.counter != self.pulses_per_cyl:
				# sync lost
				self.unsync()
				#raise Exception('Crank out of sync')
				print('Warning! Crank out of sync at t=' + str(self.crank_pc.became_act))
			else:
				#print('Fuck yea, long pulse')
				
				# reset Crank counter
				self.crank_pc.reset()

				# in sync now
				self.in_sync = True

		else:
			# regular pulse, store pulse width
			self.pulse_width = self.crank_pc.period

		# check for TDC
		if not( self.in_sync and self.crank_pc.counter == self.TDC_pulse - 1 ):
			return False

		# ***    ok, TDC detected    ***

		# prev and current TDC time, used by calculations
		this_time = self.crank_pc.became_act
		prev_time = self.prev_TDC_time

		# calculate rpm
		self.rpm = 60 / (self.time_unit * ((this_time - prev_time) * self.no_of_cyl / 2))

		# count cam pulses
		cam_pulses = list()
		for cam in self.cam_pcs:
			cam_pulses.append(cam.counter)
		#print(cam_pulses)

		# identify cylinder
		for i, (c, p) in enumerate(self.firing_order):
			if cam_pulses == p:
				# store number
				self.cylinder = c
				# store index
				cyl_index = i
				# compare with expected
				if(self.expect_cyl != 0 and self.expect_cyl != c):
					print('Warning! Expected cylinder #' + str(self.expect_cyl) + ', got #' + str(c) )
				# store next expected cyl
				self.expect_cyl = self.firing_order[ (i + 1) % self.no_of_cyl ][0]
				# exit loop
				break
		else:
			print('Warning! Cylinder not identified!')
			self.cylinder = 0
			self.expect_cyl = 0

		# futher calculations are only valid if cylinder is identified
		if self.cylinder > 0:
			# calculate current crank angle
			angle_per_cyl = 720 / self.no_of_cyl
			crank_angle = angle_per_cyl * (cyl_index + 1)

			# calculate cam advance
			for i, t in enumerate(self.cam_time):
				if t >= prev_time:					# has cam pulse arrived on this stroke?
					self.cam_angles[i] =  calc_angle(t, prev_time, 0, this_time, angle_per_cyl) - self.cam_offsets[i]	# absolute angle does not matter here

			# process advance monitors
			for i, t in enumerate(self.mon_time):
				if t >= prev_time:					# has mon pulse arrived on this stroke?
					mon_angle = calc_angle(t, prev_time, crank_angle - angle_per_cyl, this_time, crank_angle)
					self.mon_adv[i] = (self.mon_offsets[i] - mon_angle) % 720

			# store angle
			self.prev_angle = crank_angle

		# reset pulse counters
		for cam in self.cam_pcs:
			cam.reset()
		for mon in self.mon_pcs:
			mon.reset()

		# store TDC time
		self.prev_TDC_time = this_time

		return True

