import itertools
import math
import random
import numpy as np
import matplotlib.pyplot as plt

import Core
from Core import Environment
from Core.Utils.conversion import state_to_matrix
from Core.Utils.distances import manhattan_distance, x_y_distance
from .District import District


class ArmDeployment:
	"""
	Class to represent an assignment of arm to mounting points, with derived rectangular districts
	"""
	def __init__(self, env: Environment, max_district_size: int, alpha=1):
		self.env = env
		self.n_arm = self.env.n_robotic_arms
		self.max_district_size = max_district_size
		self.alpha = alpha
		self.selected_mounting_point = []
		self.available_mounting_points = list(env.mounting_points)
		self.mounting_point_tasks = None
		self.districts = None

	def random_init(self):
		"""
		Randomly choose the mounting point to deploy the arm on
		"""
		self.selected_mounting_point = random.sample(self.env.mounting_points, k=self.n_arm)
		self.available_mounting_points = []
		for m in self.env.mounting_points:
			if m not in self.selected_mounting_point:
				self.available_mounting_points.append(m)

	def get_closest(self, p: tuple):
		"""
		get the closest mounting point to a given point p
		:param p:
		:return: the closest mounting point
		"""
		closest = self.selected_mounting_point[0]
		min_distance = manhattan_distance(p, (self.selected_mounting_point[0].x, self.selected_mounting_point[0].y))
		for m_point in self.selected_mounting_point[1:]:
			distance = manhattan_distance(p, (m_point.x, m_point.y))
			if distance < min_distance:
				min_distance = distance
				closest = m_point
		return closest

	def assign_task(self):
		"""
		Assign each task to the district of the mounting point closest to the first point of the task
		"""
		self.mounting_point_tasks = {m: [] for m in self.selected_mounting_point}
		for task in self.env.tasks:
			self.mounting_point_tasks[self.get_closest(task.points[0])].append(task)

	def calculate_districts(self):
		"""
		Get the district from the mounting point chosen considering only the task that are entirely contained
		in the district they have been assigned too.
		"""
		self.districts = []
		self.assign_task()
		updated_m_point_tasks = {m: [] for m in self.selected_mounting_point}
		for m_point, tasks in self.mounting_point_tasks.items():
			max_up = 0
			max_down = 0
			max_right = 0
			max_left = 0
			for task in tasks:
				task_deleted = False
				new_max_up = max_up
				new_max_down = max_down
				new_max_right = max_right
				new_max_left = max_left
				for p in task.points:
					dist_x, dist_y = x_y_distance(p, (m_point.x, m_point.y))
					if abs(dist_x) > self.max_district_size:
						task_deleted = True
						break
					if abs(dist_y) > self.max_district_size:
						task_deleted = True
						break

					if dist_x > new_max_left:
						new_max_left = dist_x
					if -dist_x > new_max_right:
						new_max_right = -dist_x
					if dist_y > new_max_down:
						new_max_down = dist_y
					if -dist_y > new_max_up:
						new_max_up = -dist_y
				if not task_deleted:
					max_up = new_max_up
					max_down = new_max_down
					max_right = new_max_right
					max_left = new_max_left
					updated_m_point_tasks[m_point].append(task)

			self.districts.append(District(self.env, (m_point.x, m_point.y), max_up, max_down, max_right, max_left))

		self.mounting_point_tasks = updated_m_point_tasks

	def check_intersection_area(self, d1: District, d2: District) -> float:
		"""
		Get intersection area between two districts
		:param d1:
		:param d2:
		:return: the area of intersection
		"""
		dist_x = min(d1.center[0] + d1.right + 1, d2.center[0] + d2.right + 1) - max(d1.center[0] - d1.left, d2.center[0] - d2.left)
		dist_y = min(d1.center[1] + d1.up + 1, d2.center[1] + d2.up + 1) - max(d1.center[1] - d1.down, d2.center[1] - d2.down)

		if dist_x > 0 and dist_y > 0:
			return dist_x * dist_y
		else:
			return 0

	def get_intersection_over_total(self) -> float:
		"""
		calculate the sum of all the intersection areas present in the current district subdivision divided by
		the area of the environment grid
		:return: the intersection area divided by the total area
		"""
		total_inter_area = 0
		if not self.districts:
			self.calculate_districts()
		for i in range(len(self.districts)):
			for d in self.districts[i:]:
				total_inter_area += self.check_intersection_area(self.districts[i], d)
		return total_inter_area / (self.env.width * self.env.height)

	def fitness(self) -> float:
		"""
		Calculate the fitness function of the current districts subdivision. The fitness is calculated as the total number of task
		covered by the current subdivision, multiplied by the entropy of the distribution of the tasks in the districts,
		multiplied by e^(-alpha*IoT) to penalize the subdivision with high inetersection areas.
		:return: the value of fitness calculated
		"""
		if not self.districts:
			self.calculate_districts()
		total_task_covered = sum([len(tasks) for tasks in self.mounting_point_tasks.values()])
		if total_task_covered == 0:
			coverange_distrib = [0 for _ in self.selected_mounting_point]
		else:
			coverange_distrib = [len(tasks) / total_task_covered for tasks in self.mounting_point_tasks.values()]
		entropy = - sum([p * (math.log(p) if p != 0 else 0) for p in coverange_distrib])
		IoT = self.get_intersection_over_total()
		return total_task_covered * entropy * math.exp(-self.alpha * IoT)

	def reproduce(self, state, policy="random"):
		"""
		Combine the current mounting points chosen with another chose of mounting point (for genetic algorithm)
		:param state: the state representing the other chose of mounting point
		:return: the new chose of mounting points obtained by the combination of the current state with the state passed
		"""
		new_selected_mounting_point = set(self.selected_mounting_point)
		for m in state.selected_mounting_point:
			new_selected_mounting_point.add(m)
		new_selected_mounting_point = random.sample(list(new_selected_mounting_point), k=self.n_arm)
		new_state = ArmDeployment(self.env, random.choice([self.max_district_size, state.max_district_size]))
		new_state.selected_mounting_point = new_selected_mounting_point
		new_state.available_mounting_points = []
		for m in new_state.env.mounting_points:
			if m not in new_state.selected_mounting_point:
				new_state.available_mounting_points.append(m)
		return new_state

	def mutate(self):
		"""
		Mutate the current state changing one of the chosen mounting points
		:return: the current state modified
		"""
		new_mounting_point = random.choice(self.available_mounting_points)
		removed_mounting_point = random.choice(self.selected_mounting_point)
		self.selected_mounting_point.remove(removed_mounting_point)
		self.selected_mounting_point.append(new_mounting_point)
		self.max_district_size = self.max_district_size + random.randint(-5, 5)
		return self

	def get_standard_districts(self):
		if not self.districts:
			self.calculate_districts()
		standard_districts = []
		for d, m in zip(self.districts, self.selected_mounting_point):
			standard_district = Core.District((d.center[0] - d.left, d.center[1] - d.down), d.left + d.right, d.down + d.up)
			standard_district.mounting_points = [m]
			standard_district.tasks = list(self.mounting_point_tasks[m])
			standard_districts.append(standard_district)
		return standard_districts

	def get_children(self):
		shuffled_selected_mp = list(self.selected_mounting_point)
		np.random.shuffle(shuffled_selected_mp)
		shuffled_available_mp = list(self.available_mounting_points)
		np.random.shuffle(shuffled_available_mp)
		for old_m in shuffled_selected_mp:
			for new_m in shuffled_available_mp:
				new_state = ArmDeployment(self.env, max_district_size=self.max_district_size, alpha=self.alpha)
				new_state.selected_mounting_point = list(self.selected_mounting_point)
				new_state.available_mounting_points = list(self.available_mounting_points)
				new_state.selected_mounting_point.remove(old_m)
				new_state.available_mounting_points.append(old_m)
				new_state.selected_mounting_point.append(new_m)
				new_state.available_mounting_points.remove(new_m)
				yield new_state

	def draw_districts(self):
		fig, ax = plt.subplots()
		matrix = np.ones((self.env.height, self.env.width, 3)) * 0.8
		im = ax.imshow(matrix, origin="lower", cmap="seismic", interpolation="none")
		district_colors = [np.random.random(size=3) for _ in range(self.n_arm)]

		for district, color in zip(self.districts, district_colors):
			for p in itertools.product(
					range(district.center[0] - district.left, district.center[0] + district.right + 1, 1),
					range(district.center[1] - district.down, district.center[1] + district.up + 1, 1)):
				x, y = state_to_matrix(p)
				matrix[x, y, :] = color
		im.set_data(matrix)
		plt.show()
