class Raindeer:
	def __init__(self, line):
		name, _, _, speed, _, _, fly, _, _, _, _, _, _, rest, _ = line.split()
		self.name = name
		self.speed = int(speed)
		self.fly = int(fly)
		self.rest = int(rest)

	def position_at(self, t):
		period = self.fly + self.rest
		fly_time = self.fly * (t // period)
		if t % period < self.fly:
			fly_time += t % period
		else:
			fly_time += self.fly
		return fly_time * self.speed
