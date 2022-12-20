import itertools
import copy
import numpy as np
from Core.Utils.conversion import *
import random

class State:
    def __init__(self, matrix, workers, n_step=0):
        self.matrix = matrix
        self.n_worker = len(workers)
        self.workers = workers
        self.n_step = n_step
        self.f = None
        self.g = None
        self.h = None

    def __lt__(self, other):
        if not isinstance(other, State):
            raise TypeError
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def check_boundaries(self, worker, move):
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

        if new_point[0] >= np.shape(self.matrix)[1] or new_point[0] < 0:
            return False, (0, 0)
        if new_point[1] >= np.shape(self.matrix)[0] or new_point[1] < 0:
            return False, (0, 0)
        return True, new_point

    def is_move_valid(self, moves):
        """

        Args:
            robotic_arm:
            action:

        Returns:

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

            if new_worker.arm.task_points_done < new_worker.task.n_points and new_worker.arm.path[-1] == new_worker.task.points[new_worker.arm.task_points_done]:
                new_worker.arm.task_points_done += 1

            new_workers.append(new_worker)

        return True, State(self.matrix, new_workers, self.n_step + 1)

    def get_children(self):
        move_set = [["U", "D", "L", "R", "W"] for _ in range(self.n_worker)]
        moves = list(itertools.product(*move_set))
        random.shuffle(moves)
        for move in moves:
            if move == tuple(["W" for _ in range(self.n_worker)]):
                continue
            valid, new_state = self.is_move_valid(move)
            if not valid:
                continue
            # print(move)
            yield new_state
