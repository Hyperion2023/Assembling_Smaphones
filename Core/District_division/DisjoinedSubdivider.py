import itertools
import math

import matplotlib.pyplot as plt
import numpy as np
from Core.Environment import Environment
import random
from Core.Utils.conversion import state_to_matrix
from District import District


class DisjoinedSubdivider:
	def __init__(self, env: Environment, n_district):
		self.env = env
		self.n_district = n_district
		self.centers = []
		self.districts = []

	def random_init(self):
		for _ in range(self.n_district):
			center = (random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1))
			while center in self.centers:
				center = (random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1))
			self.centers.append(center)

	def draw_districts(self):
		fig, ax = plt.subplots()
		matrix = np.ones((self.env.height, self.env.width, 3)) * 0.8
		im = ax.imshow(matrix, origin="lower", cmap="seismic", interpolation="none")
		# self.ax.set_xticks([x - 0.5 for x in range(1, self.env.width)])
		# self.ax.set_yticks([y - 0.5 for y in range(1, self.env.height)])
		district_colors = [np.random.random(size=3) for _ in range(self.n_district)]
		for district, color in zip(self.districts, district_colors):
			for p in itertools.product(range(district.center[0] - district.left, district.center[0] + district.right + 1, 1), range(district.center[1] - district.down, district.center[1] + district.up + 1, 1)):
				x, y = state_to_matrix(p)
				matrix[x, y, :] = color
		im.set_data(matrix)
		plt.show()

	def district_from_centers(self):
		district = [District(self.env, c, 0, 0, 0, 0) for c in self.centers]
		self.districts = district
		updated = True
		while updated:
			# self.draw_districts()
			updated = False
			for d in district:
				if d.can_expand(district, "u"):
					d.up += 1
					updated = True
				if d.can_expand(district, "d"):
					d.down += 1
					updated = True
				if d.can_expand(district, "r"):
					d.right += 1
					updated = True
				if d.can_expand(district, "l"):
					d.left += 1
					updated = True
		self.districts = district
		# self.draw_districts()
		return district

	def get_score(self):
		if not self.districts:
			self.district_from_centers()
		district_task = {d: [] for d in self.districts}
		for task in self.env.tasks:
			district = None
			for d in self.districts:
				if d.is_in(task.points[0]):
					district = d
					break
			if not district:
				continue
			for tp in task.points[1:]:
				if not district.is_in(tp):
					district = None
					break
			if district:
				district_task[district].append(task)

		total_task_covered = sum([len(tasks) for tasks in district_task.values()])
		coverange_distrib = [len(tasks) / total_task_covered for tasks in district_task.values()]
		entropy = - sum([p * (math.log(p) if p != 0 else 0) for p in coverange_distrib])
		# min_task_dist = min([len(tasks) for tasks in district_task.values()])
		# max_task_dist = max([len(tasks) for tasks in district_task.values()])
		return total_task_covered * entropy

	def reproduce(self, state2):
		starting_point = 0
		end_point = self.n_district - 1
		split_point = random.randint(starting_point, end_point)
		new_centers = self.centers[0:split_point] + state2.centers[split_point:]
		new_state = DisjoinedSubdivider(self.env, self.n_district)
		new_state.centers = new_centers
		return new_state

	def mutate(self):
		mutating_district = random.randint(0, self.n_district - 1)
		self.centers[mutating_district] = (
			random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1))
		return self

	def fitness(self):
		return self.get_score()
