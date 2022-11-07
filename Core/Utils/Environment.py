from District import District
from RoboticArm import RoboticArm

class Environment:
    def __init__(self, width, height, n_robotic_arms=0, district_size=2):

        self.width = width
        self.height = height
        self.districts = []
        self.district_size = district_size

        # subdivide the grid in district
        # if the width or height is not a multiple of district_size extend the last district to cover the grid
        for i in range(self.width, step=district_size):
            column = []
            if self.width - i < 2 * district_size:
                size_x = self.width - i
            else:
                size_x = district_size
            for j in range(self.height, step=district_size):
                if self.height - j < 2 * district_size:
                    size_y = self.height - j
                else:
                    size_y = district_size
                new_district = District((i, j), size_x, size_y)
                column.append(new_district)
            self.districts.append(column)

        self.tasks = []
        self.mounting_points = []
        self.n_robotic_arms = n_robotic_arms
        self.robotic_arms = []

    def add_task(self, task):
        self.tasks.append(task)
        first_point = task.points[0]
        self.calculate_district(first_point[0], first_point[1]).add_task(task)

    def calculate_district(self, x, y):
        dx, dy = int(x / self.district_size), int(y / self.district_size)
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

    def move_robotic_arm(self, robotic_arm, action):
        if action not in ["U", "R", "D", "L", "W"]:
            raise ValueError("action must be one of U R D L W")

        last_point = robotic_arm.path[-1]
        if action == "U":
            new_point = (last_point[0], last_point[1] + 1)
        elif action == "R":
            new_point = (last_point[0] + 1, last_point[1])
        elif action == "D":
            new_point = (last_point[0], last_point[1] - 1)
        elif action == "L":
            new_point = (last_point[0] - 1, last_point[1])
        else:  # action is W
            robotic_arm.moves.append(action)
            return

        if new_point[0] > self.width or new_point[0] < 0:
            raise ValueError("invalid move, width exceeded")
        if new_point[1] > self.height or new_point[1] < 0:
            raise ValueError("invalid move, height exceeded")

        robotic_arm.moves.append(action)
        robotic_arm.path.append(new_point)


