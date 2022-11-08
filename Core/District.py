class District:
    def __init__(self, origin, width, height):
        self.origin = origin
        self.width = width
        self.height = height
        self.task = []
        self.mounting_points = []
        self.robotic_arm = []

    def add_task(self, task):
        self.task.append(task)

    def add_mounting_point(self, mounting_point):
        self.mounting_points.append(mounting_point)

    def add_robotic_arm(self, robotic_arm):
        self.robotic_arm.append(robotic_arm)
