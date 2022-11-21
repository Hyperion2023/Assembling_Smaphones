class Task:
    def __init__(self, value=0, n_points=0):
        self.value = value
        self.n_points = n_points
        self.points = []
        self.distance = 0

    @staticmethod
    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    @staticmethod
    def x_y_distance(p1, p2):
        return (p2[0] - p1[0],p2[1] - p1[1])

    def add_point(self, x, y):
        if len(self.points) == self.n_points:
            raise ValueError("Number of points execeeded!")
        self.update_distance(x, y)  # update_distance must be called before adding point
        self.points.append((x, y))

    def update_distance(self, x, y):
        if len(self.points) == 0:
            return
        last_point = self.points[-1]
        self.distance += self.manhattan_distance(last_point, (x, y))

    def get_task_score(self, mounting_point):
        first_point = self.points[0]
        self.score= self.value / (self.distance + self.manhattan_distance(first_point, (mounting_point.x, mounting_point.y)))
        #print("SCORE: "+str(self.score))
        return self.score

    def task_completed(self):
        
        if len(self.points)==0:
            print("TASK Completed")
            return True
        else:
            print("TASK len still in progress")
            return False

    def task_target_update(self):
        self.points.pop(0)
        self.n_points-=1

    def get_distance_to_first_point(self,position):        
        return self.x_y_distance(position,self.points[0])
    def get_position(self):
        return self.points[0]

    
