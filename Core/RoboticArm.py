class RoboticArm:
    def __init__(self):
        self.mounting_point = None
        self.path = []
        self.moves = []
        self.collision_check = False
        self.task_points_done = 0

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

    def mount(self, mounting_point):
        self.mounting_point = mounting_point
        mounting_point.occupied = True
        self.path.append((mounting_point.x, mounting_point.y))
    def get_position(self):
        return self.path[-1]
    def retract_all(self):
        return 0