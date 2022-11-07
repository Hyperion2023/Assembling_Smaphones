from District import District


class Environment:
    def __init__(self, width, height, n_robotic_arms=0, district_size=2):
        self.width = width
        self.height = height

        self.districts = []

        # subdivide the grid in district
        # if the width or height is not a multiple of district_size extend the last district to cover the grid
        for i in range(self.width, step=district_size):
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
                self.districts.append(new_district)

        self.tasks = []
        self.mounting_points = []
        self.n_robotic_arms = n_robotic_arms

    def add_task(self, task):
        self.tasks.append(task)

