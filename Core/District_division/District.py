class District:
	def __init__(self, env, center, up, down, right, left):
		self.env = env
		self.center = center
		self.up = up
		self.down = down
		self.right = right
		self.left = left

	def can_expand(self, districts, direction):
		if direction == "u":
			points = [(i, self.center[1] + self.up + 1) for i in
			          range(self.center[0] - self.left, self.center[0] + self.right + 1, 1)]
		elif direction == "d":
			points = [(i, self.center[1] - self.down - 1) for i in
			          range(self.center[0] - self.left, self.center[0] + self.right + 1, 1)]
		elif direction == "r":
			points = [(self.center[0] + self.right + 1, i) for i in
			          range(self.center[1] - self.down, self.center[1] + self.up + 1, 1)]
		elif direction == "l":
			points = [(self.center[0] - self.left - 1, i) for i in
			          range(self.center[1] - self.down, self.center[1] + self.up + 1, 1)]
		else:
			raise Exception()
		for p in points:
			if not self.env.width > p[0] >= 0 or not self.env.height > p[1] >= 0:
				return False
			for district in districts:
				if district.is_in(p):
					return False
		return True

	def is_in(self, p):
		if self.center[0] + self.right >= p[0] >= self.center[0] - self.left and self.center[1] + self.up >= p[
			1] >= self.center[1] - self.down:
			return True
		else:
			return False
