class District:
    def __init__(self, origin, width, height):
        self.origin = origin
        self.width = width
        self.height = height
        self.task = []
        self.mounting_points = []

    def add_task(self, task):
        self.task.append(task)

    def add_mounting_point(self, mounting_point):
        self.mounting_points.append(mounting_point)