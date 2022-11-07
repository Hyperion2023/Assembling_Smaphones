class Task:
    def __init__(self,value=0,n_points=0):
        self.value=value
        self.n_points=n_points
        self.points=[]

    def add_point(self,x,y):
        if len(self.points)==self.n_points:
            raise ValueError("Number of points execeeded!")
        self.points.append((x,y))
    
    def get_task_score(self):
        # TODO: compute manhattan distance between points of tasks in correct order 
        
        pass
