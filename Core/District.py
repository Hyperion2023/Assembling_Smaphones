class District:
    def __init__(self, origin, width, height):
        self.origin = origin
        self.width = width
        self.height = height
        self.tasks = []
        self.mounting_points = []
        self.robotic_arms = []
        self.ordered_tasks = [] #List of lists<

    def add_task(self, task):
        self.tasks.append(task)

    def add_mounting_point(self, mounting_point):
        self.mounting_points.append(mounting_point)

    def sort_tasks(self):
        self.ordered_tasks = []
        for mounting_point in self.mounting_points:
            new_list = list(self.tasks)
            new_list.sort(key=lambda x: x.get_task_score(mounting_point), reverse=True)
            self.ordered_tasks.append(new_list)

    def add_robotic_arm(self, robotic_arm):
        self.robotic_arms.append(robotic_arm)
