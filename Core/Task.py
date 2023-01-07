from Core.Utils.distances import manhattan_distance, x_y_distance
from Core import MountingPoint


class Task:
    """
    Class tha represents a Task and contains it value and the positions of its points.

    Attributes
    ----------
    value : int
        The value of the task.
    n_points : int
        The number of points in the task.
    points : list[tuple[int, int]]
        The coordinates of the points of the task.
    distance : int
        The distance between the points of the task.
    score : float
        The score of the task with respect to the considered starting point.
    """
    def __init__(self, value: int = 0, n_points: int = 0):
        """
        Constructor of the class Task.
        :param value: Value gained from completing the task. (Default: 0)
        :param n_points: Number of sub-points required to visit in order to complete the task. (Default :0)
        """
        self.value = value
        self.n_points = n_points
        self.points = []
        self.distance = 0
        self.score = 0

    @property
    def show_task(self):
        """Print all the task points."""
        for i in self.points:
            print(i)

    def add_point(self, x: int, y: int):
        """
        Adds a tuple of coordinates in the correct order to the list of points to visit in order to complete the task.
        :param x: X coordinate.
        :param y: Y coordinate.
        """
        if len(self.points) == self.n_points:
            raise ValueError("Number of points execeeded!")
        self.update_distance(x, y)  # update_distance must be called before adding point
        self.points.append((x, y))

    def update_distance(self, x, y):
        """
        Method that computes the distance between a given point and the first point of the tasks and then adds all the
        distances between two consecutive points in the points list. This gives a metric of the minimum total distance
        that and arm needs to cover in order to complete the task.
        :param x: X point coordinate.
        :param y: Y point coordinate.
        :return: If there are no points in the list the function returns nothing.
        """
        if len(self.points) == 0:
            return
        last_point = self.points[-1]
        self.distance += manhattan_distance(last_point, (x, y))

    def get_task_score(self, mounting_point: MountingPoint) -> float:
        """
        Method that computes a metric to sort the different tasks for each mounting point.
        Given the total distance wrt the mounitng point position and the value of the task once completed, it computes
        and return a score.
        :param mounting_point: Mounting Point.
        :return: Score value.
        """
        first_point = self.points[0]
        self.score = self.value / (
                self.distance + manhattan_distance(first_point, (mounting_point.x, mounting_point.y)))
        #print("SCORE: "+str(self.score))
        return self.score

    def task_completed(self) -> bool:
        """
        Method that checks if a task is/has been completed.
        :return: True if the task is completed, orhterwise False.
        """
        if len(self.points) == 0:
            # print("TASK Completed")

            return True
        else:
            # print("TASK len still in progress")
            return False

    def task_target_update(self):
        """
        Method that removes the first point in the points list and decreases the number of total point to cover of the
        given task.
        """
        self.points.pop(0)
        self.n_points -= 1

    def get_distance_to_first_point(self, position: tuple) -> int:
        """
        Method that computes the distance between the point given in input and the first point in the point list.
        :param position: x,y coordinates of a point.
        :return: Distance.
        """
        return x_y_distance(position, self.points[0])

    def get_distance_between_two_points(self, index1: tuple, index2: tuple) -> int:
        """
        Mehtod that computes the distance between two points
        :param index1: First point.
        :param index2: Second point.
        :return: Distance between the two points.
        """
        return x_y_distance(self.points[index1], self.points[index2])

    def get_distance_to_all_points(self, starting_position: tuple) -> list:
        """
        Computes the distances between a given point and all the points of the tasks.
        In particular, it computes the distance between the starting_position and the first point, and the form the first
        point to the second, and so on until the last one. All these distances are then appended and returned in a list
        :param starting_position: X,Y coordinate of the starting point.
        :return: List of distances
        """
        res = [self.get_distance_to_first_point(starting_position)]
        for index1 in range(0, len(self.points) - 1):
            res.append(self.get_distance_between_two_points(index1, index1+1))
        return res

    @property
    def get_position(self):
        """get the position of the first point."""
        return self.points[0]

    
