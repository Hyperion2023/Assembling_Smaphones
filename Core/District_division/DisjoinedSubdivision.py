import itertools
import math
import random
import matplotlib.pyplot as plt
import numpy as np

from Core import Environment
from Core.Utils.conversion import state_to_matrix
from .District import District


class DisjoinedSubdivision:
	"""
	Class that represent a subdivision of the environment grid in disjoined rectangular districts
	"""
	def __init__(self, env: Environment, n_district: int):
		self.env = env
		self.n_district = n_district
		self._centers = []
		self.districts = []

	def random_init(self):
		"""
		Initialize randomly the position of centers of districts
		"""
		for _ in range(self.n_district):
			center = (random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1))
			while center in self._centers:
				center = (random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1))
			self._centers.append(center)

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
		"""
		Generate the districts from the position of the centers
		:return: the generated districts
		"""
		district = [District(self.env, c, 0, 0, 0, 0) for c in self._centers]
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

	def reproduce(self, state):
		"""
		Combine the representation of the subdivision with another subdivision (for genetic algorithm)
		:param state:
		:return: the new state obtained by the combination of the current state with the state passed
		"""
		starting_point = 0
		end_point = self.n_district - 1
		split_point = random.randint(starting_point, end_point)
		new_centers = self._centers[0:split_point] + state._centers[split_point:]
		new_state = DisjoinedSubdivision(self.env, self.n_district)
		new_state._centers = new_centers
		return new_state

	def mutate(self):
		"""
		Mutate the current state changing the position of one center of a district
		:return: the current state modified
		"""
		mutating_district = random.randint(0, self.n_district - 1)
		self._centers[mutating_district] = (
			random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1))
		return self

	def fitness(self) -> float:
		"""
		Calculate the fitness function of the current subdivision. The fitness is calculated as the total number of task
		covered by the current subdivision, multiplied by the entropy of the distribution of the tasks in the districts.
		:return: the value of fitness calculated
		"""
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
