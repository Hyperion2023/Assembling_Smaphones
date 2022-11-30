from Core.District import District
from Core.RoboticArm import RoboticArm
from Core.MoutingPoint import MountingPoint
from Core.Task import Task
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

class Environment:
    def __init__(self, width, height, n_steps, n_robotic_arms, district_size=17):

        self.width = width
        self.height = height
        self.districts = []  # this will be a list of list
        self.district_size = district_size
        self.n_steps = n_steps
        self.current_step = 0
        self.fig = plt.figure()
        plt.switch_backend('TkAgg')  # TkAgg (instead Qt4Agg)
        plt.get_backend()
        self.matrix = np.ones((self.height, self.width, 3))*0.6
        self.im = plt.imshow(self.matrix, origin="lower", cmap="seismic", interpolation="none")
        self.ax = plt.gca()
        self.ax.set_xticks([x - 0.5 for x in range(1, self.width)])
        self.ax.set_yticks([y - 0.5 for y in range(1, self.height)])
        #plt.grid()
        mng = plt.get_current_fig_manager()
        ### works on Ubuntu??? >> did NOT working on windows
        mng.resize(*mng.window.maxsize())

        # subdivide the grid in district
        # if the width or height is not a multiple of district_size extend the last district to cover the grid
        for i in range(0, self.width, district_size):
            row = []
            if self.width - i <  district_size:
                break
            if self.width - i < 2 * district_size:
                size_x = self.width - i
            else:
                size_x = district_size
            for j in range(0, self.height, district_size):
                if self.height - j < district_size:
                    break
                if self.height - j < 2 * district_size:
                    size_y = self.height - j
                else:
                    size_y = district_size
                new_district = District((i, j), size_x, size_y)
                row.append(new_district)
            self.districts.append(row)

        self.tasks = []
        self.mounting_points = []
        self.n_robotic_arms = n_robotic_arms
        self.robotic_arms = []
        self.total_score = 0

    def add_tasks(self, tasks, task_positions):
        for task, positions in zip(tasks, task_positions):
            t = Task(int((task.split(" "))[0]), int((task.split(" "))[1]))
            for index in range(0, t.n_points * 2, 2):
                t.add_point(int((positions.split(" "))[index]), int((positions.split(" "))[index + 1]))
            self.tasks.append(t)
            first_point = t.points[0]
            self.calculate_district(first_point[0], first_point[1]).add_task(t)

    def calculate_district(self, x, y):
        dx, dy = int(x / self.district_size), int(y / self.district_size)
        if dx > len(self.districts) - 1:
            dx = len(self.districts) - 1
        if dy > len(self.districts[0]) - 1:
            dy = len(self.districts[0]) - 1
        return self.districts[dx][dy]

    def add_robotic_arm(self, mounting_point):
        if len(self.robotic_arms) == self.n_robotic_arms:
            raise ValueError("max number of robotic arm already reached!")

        if mounting_point.occupied:
            raise ValueError("mounting point already occupied")

        arm = RoboticArm()
        arm.mount(mounting_point)
        self.robotic_arms.append(arm)
        self.calculate_district(mounting_point.x, mounting_point.y).add_robotic_arm(arm)
        return arm

    def add_mounting_points(self, mounting_points):
        for m in mounting_points:
            mounting_point = MountingPoint(m[0], m[1])
            self.mounting_points.append(mounting_point)
            self.calculate_district(mounting_point.x, mounting_point.y).add_mounting_point(mounting_point)

    def update_time(self):
        print("°°°°°°°°°°°°°°˚°°°°°°°°TIME UPDATED°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        for a in self.robotic_arms:
            if len(a.moves) - 1 < self.current_step:
                a.moves.append("W")
        self.current_step += 1

    def move_robotic_arm(self, robotic_arm, action):
        """

        Args:
            robotic_arm:
            action:
            new_point:
        """
        valid, new_point = self.is_move_valid(robotic_arm, action)
        if not valid:
            return False
        robotic_arm.moves.append(action)
        robotic_arm.path.append(new_point)
        return True


    def is_move_valid(self, robotic_arm, action):
        """

        Args:
            robotic_arm:
            action:

        Returns:

        """
        if action not in ["U", "R", "D", "L", "W"]:
            raise ValueError("action must be one of U R D L W")
        # print("MOVES: "+ str(len(robotic_arm.moves)))
        # print("MOVES index: "+ str(self.current_step))
        if len(robotic_arm.moves) > self.current_step:
            # print("TOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            # print(len(robotic_arm.moves))

            return False, (0, 0)
        flag = False
        last_point = robotic_arm.path[-1]
        # print("ARM LASTPOINT: " + str(last_point))
        if action == "U":
            new_point = (last_point[0], last_point[1] + 1)
        elif action == "R":
            new_point = (last_point[0] + 1, last_point[1])
        elif action == "D":
            new_point = (last_point[0], last_point[1] - 1)
        elif action == "L":
            new_point = (last_point[0] - 1, last_point[1])
        else:
            new_point = last_point

        if len(robotic_arm.path) >= 2:
            if new_point == robotic_arm.path[-2]:
                flag = True
        # print("NEWPOINT: " +str(new_point))
        if not flag:
            if new_point[0] > self.width or new_point[0] < 0:
                return False, (0, 0)
            if new_point[1] > self.height or new_point[1] < 0:
                return False, (0, 0)

            # check if new_point is on a mounting point
            for m in self.mounting_points:
                if new_point[0] == m.x and new_point[1] == m.y:
                    return False, (0, 0)

            # check if new_point collide with another robotic arm
            for a in self.robotic_arms:
                for p in a.path:
                    if new_point == p:
                        return False, (0, 0)
        else:

            robotic_arm.path.pop()
            new_point = robotic_arm.path[-1]
            robotic_arm.path.pop()

        return True, new_point

    def show(self):
        print(self.width, self.height, self.n_robotic_arms, len(self.mounting_points), len(self.tasks), self.n_steps,
              sep=" ")
        for point in self.mounting_points:
            print(point.x, point.y, sep=" ")
        for task in self.tasks:
            print(task.value, task.n_points, sep=" ")
            for point in task.points:
                print(point[0], point[1], sep=" ", end=" ")
            print(" ")

    def draw(self, agent=None):
        self.matrix = np.ones((self.height, self.width, 3))*0.8


        for t in self.tasks:
            for inner in t.points:
                self.matrix[inner[1], inner[0]] = (0, 0, 1)
        if agent:
            for t in agent.running_workers:
                for inner in t.task.points:
                    self.matrix[inner[1], inner[0]] = (0, 0.5, 1)
        for r in self.robotic_arms:
            for index, points in enumerate(r.path):
                if index != len(r.path)-1:
                    self.matrix[points[1], points[0]] = (1, 1-0.4*((index+1)/len(r.path)), 1-0.8*((index+1)/len(r.path)))
                else:
                    self.matrix[points[1], points[0]] = (1, 0.5,0)

        for m in self.mounting_points:
            self.matrix[m.y, m.x] = (1, 0, 0)
        self.im.set_data(self.matrix)
        for row in self.districts:
            for district in row:
                self.ax.add_patch(patches.Rectangle((district.origin[0]-0.5,district.origin[1]-0.5), district.width, district.height, linewidth=1, edgecolor='b', facecolor='none'))

        plt.draw()
        plt.pause(1)
