from Core import MountingPoint


class RoboticArm:
    """
    Class that represents a Robotic arm. It can mount it and check if the action si valid.
    ...
    Attributes
    ----------
    mounting_point : Core.MountingPoint.MountingPoint
        Mounting point of the arm.
    path : list[tuple[int, int]]
        Path of the arm.
    moves : list[str]
        Set of moves performed on the arm.
    collision_check : bool
        Check if the arm is collision free.
    graph : Core.Utils.Dijkstra.Graph
        Dijkstra graph from the mounting point.
    """
    def __init__(self):
        """
        Constructor of the RoboticArm class.
        """
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