from Core.Environment import Environment
from Core.MoutingPoint import MountingPoint
from Core.Planner.Path import OptimalPath
from Core.RoboticArm import RoboticArm
from Core.Task import Task


class Worker:
    def __init__(self, arm: RoboticArm, task: Task, env):
        self.arm = arm
        self.task = task
        self.plan = []  # TODO: implement in future version
        self.action_taken = False
        self.env = env
        self.generate_optimal_path()

    def generate_optimal_path(self):
        self.optimal_path = OptimalPath(self.env)
        self.optimal_path.compute_path(self.arm.mounting_point, self.task)
        print("Starting From:")
        print(self.arm.mounting_point.x, self.arm.mounting_point.y)
        print("#########Destinations###########")
        self.task.show_task
        print("#########PATH###########")

        for positions in self.optimal_path.path:
            print(positions)

        print("-------------------------------------")

    def my_description(self):
        print("Arm mounted in x: " + str(self.arm.mounting_point.x) + " y: " + str(self.arm.mounting_point.y))
        print("Task assigned with value: ", self.task.value)
        for i in self.task.points:
            print(" Passing through point x: ", i[0], " y: ", i[1])

    def take_action(self):
        self.action_taken = True

    def reset_action_taken(self):
        self.action_taken = False

    def retract(self):
        if not self.arm.collision_check:
            if len(self.arm.path) > 1:

                return True, self.arm.path[-2]
            else:

                return False, self.arm.path[-1]

        else:
            return False, (0, 0)  # TODO: to modify for real collision_check
