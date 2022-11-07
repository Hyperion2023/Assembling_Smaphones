class RoboticArm:
    def __init__(self, mounting_point):
        self.mounting_point = mounting_point
        mounting_point.occupied = True
        self.path = []
        self.moves = []

    # TODO move this method in the environment class
    @staticmethod
    def check_action(new_point, environment):
        if new_point[0] > environment.widht or new_point[0] < 0:
            return False
        if new_point[1] > environment.height or new_point[1] < 0:
            return False
        for m in environment.mounting_points:
            if m == new_point:
                return False

        for r in environment.robotic_arms:
            for p in r.path:
                if p == new_point:
                    return False

    def move(self, action, environment):
        if action not in ["U", "R", "D", "L", "W"]:
            raise ValueError("action must be one of U R D L W")
        self.moves.append(action)

        last_point = self.path[-1]
        if action == "U":
            self.path.append((last_point[0], last_point[1] + 1))
        elif action == "R":
            self.path.append((last_point[0] + 1, last_point[1]))
        elif action == "D":
            self.path.append((last_point[0], last_point[1] - 1))
        elif action == "L":
            self.path.append((last_point[0] - 1, last_point[1]))
