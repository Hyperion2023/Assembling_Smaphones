

import numpy as np

class Data:
    """" A class used to represent the data of the problem

    Attributes:
    
    router_range
    backbone_cost
    router_cost
    budget
    initial_backbone: touple containing the initial access point for the backbone
    matrix: a 2D numpy.array of char values 
    target_area: the number of "." in the matrix


    """

    
    
    def __init__(self, file_path : str):
        
        with open(file_path, "r") as f:
            lines = f.readlines()

            self.width = int((lines[0].split(" "))[0])
            self.height = int((lines[0].split(" "))[1])
            self.number_of_arms =  int((lines[0].split(" "))[2])
            self.number_of_mouting_points = int((lines[0].split(" "))[3])
            self.number_of_tasks =  int((lines[0].split(" "))[4])
            self.number_of_total_steps =  int((lines[0].split(" "))[5])

            self.mouting_points = [ (int((s.split(" "))[0]), int((s.split(" "))[1])) for s in lines[1:self.number_of_mouting_points]]

            tasks=lines[self.number_of_mouting_points+1:]
            for

            python_matrix = []
            for line in lines:
                python_matrix.append([str(c) for c in line][:len(line)-1])
            
            self.matrix = np.array(python_matrix, dtype=str)
            
            self.target_area = np.count_nonzero(self.matrix == ".")