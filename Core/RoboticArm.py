from Core import MountingPoint


class RoboticArm:
    """
    Class that represents a Robotic arm. It can mount it and check if the action si valid.
    """
    def __init__(self):
        self.mounting_point = None
        self.path = []
        self.moves = []
        self.collision_check = False
        self.graph = None

    def mount(self, mounting_point: MountingPoint):
        """
        Method that mounts an arm on a mounting point.
        :param mounting_point: Mouting Point.
        """
        self.mounting_point = mounting_point
        self.path.append((mounting_point.x, mounting_point.y))

    def get_position(self):
        return self.path[-1]