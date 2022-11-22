from Core.Task import Task
from Core.MoutingPoint import MountingPoint
from Core.RoboticArm import RoboticArm


class Worker:
    def __init__(self, arm: RoboticArm, task: Task):
        self.arm = arm
        self.task = task
        self.plan = [] # TODO: implement in future version
        self.action_taken=False

    def my_description(self):
        print("Arm mounted in x: " + str(self.arm.mounting_point.x) + " y: " + str(self.arm.mounting_point.y))
        print("Task assigned with value: ", self.task.value)
        for i in self.task.points:
            print(" Passing through point x: ", i[0], " y: ", i[1])

    def take_action(self):
        self.action_taken=True
    
    def reset_action_taken(self):
        self.action_taken=False

    def retract(self):
        if not self.arm.collision_check:
            if len(self.arm.path)>1:
         
                return True, self.arm.path[-2]
            else:

                return False, self.arm.path[-1]
            
        else:
            return False,(0,0)#TODO: to modify for real collision_check




