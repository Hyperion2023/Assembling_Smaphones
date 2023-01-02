import itertools
import copy
import numpy as np
import random

import Core
from Core.Utils.conversion import *
from Core import Worker


class State:
	"""
	Class that represent a state of the problem, consisting of the grid (immutable and shared between all states)
	and the workers that are present in the problem
	"""
	def __init__(self, matrix: np.array, workers: list, n_step: int = 0):
		self.matrix = matrix
		self.n_worker = len(workers)
		self.workers = workers
		self.n_step = n_step
		self.f = None
		self.g = None
		self.h = None

	def __lt__(self, other: object) -> bool:
		"""
		Compare the state with another state considering the value of f.
		:param other: the state to compare with
		:return: true if f is smaller (on equal f the value of h is considered)
		"""
		if not isinstance(other, State):
			raise TypeError
		if self.f == other.f:
			return self.h < other.h
		else:
			return self.f < other.f

	def check_boundaries(self, worker: Worker, move: str) -> tuple:
		"""
		Chek if a move would make an arm head finish out of the district.
		:param worker: the worker associated with the arm making the move
		:param move: the move to be checked
		:return: a tuple containing True in the first element if the move can be done, False otherwise.
		The second element is the new point where the head of the arm is after the move (if the move can be done).
		"""
		last_point = worker.arm.path[-1]
		# print("ARM LASTPOINT: " + str(last_point))
		if move == "U":
			new_point = (last_point[0], last_point[1] + 1)
		elif move == "R":
			new_point = (last_point[0] + 1, last_point[1])
		elif move == "D":
			new_point = (last_point[0], last_point[1] - 1)
		elif move == "L":
			new_point = (last_point[0] - 1, last_point[1])
		else:
			new_point = last_point

		if new_point[0] < worker.district.origin[0] or new_point[0] > worker.district.origin[0] + worker.district.width:
			return False, (0, 0)
		if new_point[1] < worker.district.origin[1] or new_point[1] > worker.district.origin[1] + worker.district.height:
			return False, (0, 0)
		return True, new_point

	def is_move_valid(self, moves: tuple) -> tuple:
		"""
		Check if all the moves in the provided list (one for each worker) are valid, considering the boundaries of the grid,
		the collision with other arms and the collision with mounting point.
		:param moves: the list of moves specified in the same order of the workers present in the state
		:return: a tuple containing True in the first element if all the moves can be done, False otherwise.
		The second element is the new state generated from the current one after doing the moves.
		If the moves are not valid return None.
		"""
		retracted_workers = []
		new_points = []
		for worker, move in zip(self.workers, moves):
			valid, new_point = self.check_boundaries(worker, move)
			if not valid:
				return False, None

			if len(worker.arm.path) >= 2 and new_point == worker.arm.path[-2]:
				retracted_workers.append(worker)
			# check if new_point is on a mounting point
			elif tuple(self.matrix[state_to_matrix(new_point)]) == (1, 0, 0):  # value for mounting point
				return False, None
			# check collision with other arms
			for other_w in self.workers:
				for p in other_w.arm.path[:-2 if other_w in retracted_workers else len(other_w.arm.path)]:
					if p == new_point:
						return False, None

			# Check for new points collision, continue only if new point does not collide with other new points.
			# If false then append newpoint to newpoints list
			if new_point in new_points:
				return False, None
			new_points.append(new_point)

		new_workers = []
		for worker, move, point in zip(self.workers, moves, new_points):
			new_worker = copy.deepcopy(worker)
			new_worker.arm.moves.append(move)

			if worker in retracted_workers:
				new_worker.arm.path.pop()
			else:
				new_worker.arm.path.append(point)

			if new_worker.task_points_done < new_worker.task.n_points and new_worker.arm.path[-1] == \
					new_worker.task.points[new_worker.task_points_done]:
				new_worker.task_points_done += 1

			new_workers.append(new_worker)

		return True, State(self.matrix, new_workers, self.n_step + 1)

	def get_children(self):
		"""
		Yield al the possible state that can be obtained by the current state doing valid moves.
		"""
		move_set = [["U", "D", "L", "R", "W"] for _ in range(self.n_worker)]
		moves = list(itertools.product(*move_set))
		random.shuffle(moves)
		for move in moves:
			if move == tuple(["W" for _ in range(self.n_worker)]):
				continue
			valid, new_state = self.is_move_valid(move)
			if not valid:
				continue
			yield new_state
