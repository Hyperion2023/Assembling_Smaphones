from Core import MountingPoint, RoboticArm, Task


class District:
    """
    District class. A district is a spatial subdivision of the original matrix
    """
    def __init__(self, origin: tuple, width: int, height: int):
        """
        Constructor of the District class.
        :param origin: Tuple of points that indicate the bottom left point of the district area.
        :param width: Integer that indicates how wide the district is.
        :param height: Integer that indicates how high the district is.
        """
        self.origin = origin
        self.width = width
        self.height = height
        self.tasks = []
        self.mounting_points = []
        self.robotic_arms = []
        self.ordered_tasks = [] #List of lists<

    def add_task(self, task: Task):
        """
        Method to add the tasks contained in the district
        :param task: A task in the district.
        """
        self.tasks.append(task)

    def add_mounting_point(self, mounting_point: MountingPoint):
        """
        Method to add a mounting point that is contained in the district.
        :param mounting_point: A mounting point that is contained in the district.
        """
        self.mounting_points.append(mounting_point)

    def sort_tasks(self):
        """
        This methods generates a list of lists in which for each mounting point in the district, the tasks in the
        district are sorted considering the best profitable way to complete them considering the distance and the total
        points each tasks awards, starting form a given mounting point.
        """
        self.ordered_tasks = []
        for mounting_point in self.mounting_points:
            new_list = list(self.tasks)
            new_list.sort(key=lambda x: x.get_task_score(mounting_point), reverse=True)
            self.ordered_tasks.append(new_list)

    def add_robotic_arm(self, robotic_arm: RoboticArm):
        """
        Method to add a robotic arm that is contained in the district.
        :param robotic_arm: A robotic arm that is mounted on a mounting point in the district.
        """
        self.robotic_arms.append(robotic_arm)
