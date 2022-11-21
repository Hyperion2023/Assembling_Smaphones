from Core.Task import Task
from Core.MoutingPoint import MountingPoint
from Core.RoboticArm import RoboticArm


class Worker:
    def __init__(self, arm: RoboticArm, task: Task):
        self.arm = arm
        self.task = task
        self.plan = []

    def my_description(self):
        print("Arm mounted in x: " + str(self.arm.mounting_point.x) + " y: " + str(self.arm.mounting_point.y))
        print("Task assigned with value: ", self.task.value)
        for i in self.task.points:
            print(" Passing through point x: ", i[0], " y: ", i[1])


