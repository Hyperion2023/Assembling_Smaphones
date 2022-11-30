sign = lambda x: 1 - 2 * (x < 0)


class OptimalPath:

    def __init__(self, env, id=0):
        self.path = []
        self.moves = []
        self.id = id
        self.env = env

    def compute_path(self, mouting_point, task):
        current_point = (mouting_point.x, mouting_point.y)
        points = task.points
        self.distances = task.get_distance_to_all_points((mouting_point.x, mouting_point.y))
        print("######ààà############POINTS")
        print(points)
        print("###################DISTANCES")
        for distance in self.distances:
            print(distance)
        for distance_index, point in enumerate(points):
            print("######################################################################################")
            distance = self.distances[distance_index]
            while current_point[0]!=point[0] or current_point[1]!=point[1]: #fino a che non raggiungo il punto
                moved=0
                x_dist,y_dist=task.x_y_distance(current_point,point)
                if x_dist!=0:
                    temp_current_point = (current_point[0] + sign(distance[0]), current_point[1])
                    points_to_add= self.valid_or_subpath("R" if sign(distance[0]) >0 else "L",temp_current_point,point,task)
                    current_point = points_to_add
                    self.path.append(points_to_add)
                    moved=1
                if not moved and y_dist!=0:
                    temp_current_point = (current_point[0], current_point[1] + sign(distance[1]))
                    points_to_add = self.valid_or_subpath("D" if sign(distance[0]) >0 else "U",temp_current_point,point,task)
                    current_point = points_to_add
                    self.path.append(points_to_add)
            print("POINT " + str(point[0]) + "," + str(point[1]) + " REACHED")

    def valid_or_subpath(self, moveType, point,dest,task):
        print("VALIDORSUBPATH")
        print(point)

        print(self.env.matrix[point[1],point[0]])

        if not (self.env.matrix[point[1],point[0]] == (1, 0, 0)).all():
            return point
        elif moveType=="U":
            print("U")
            if task.manhattan_distance((point[0]-1,point[1]-1),dest) >task.manhattan_distance((point[0]-1,point[1]+1),dest):
                point= (point[0]-1,point[1]+1)
            else:
                point = (point[0] - 1, point[1] - 1)
            return point
        elif moveType=="D":
            print("D")
            if task.manhattan_distance((point[0] + 1, point[1] - 1), dest) > task.manhattan_distance(
                    (point[0] + 1, point[1] + 1), dest):
                point = (point[0] + 1, point[1] + 1)
            else:
                point = (point[0] + 1, point[1] - 1)
            return point
        elif moveType=="L":
            print("L")
            if task.manhattan_distance((point[0] - 1, point[1] - 1), dest) > task.manhattan_distance(
                    (point[0] + 1, point[1] - 1), dest):
                point = (point[0] + 1, point[1] - 1)
            else:
                point = (point[0] - 1, point[1] - 1)
            return point
        elif moveType=="R":
            print("R")
            if task.manhattan_distance((point[0] - 1, point[1] + 1), dest) > task.manhattan_distance(
                    (point[0] + 1, point[1] + 1), dest):
                point = (point[0] - 1, point[1] + 1)
            else:
                point = (point[0] + 1, point[1] + 1)
            return point





