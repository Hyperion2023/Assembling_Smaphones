import random

from Core import Worker, Environment
from alive_progress import alive_bar
from Core.Utils.conversion import global_coordinates_to_district_coordinates

drawFlag = True
sec_time = 10
from Core.Utils.Dijkstra import *

class Agent:
    """
    Class that represents the Agent responsible for supervising all the workers in the environment.

    Attributes
    ----------
    environment : Core.Environment.Environment
        Environment object that represents the current state of the environment.
    n_total_arms : int
        Total number of arms in the environment.
    running_workers : list[Core.Worker.Worker]
        List of workers that are currently running.
    deployed_arms: int
        Total number of arms deployed in the environment.
    """

    def __init__(self, environment: Environment):
        """
        Agent Class constructor. It imports the environment in which the agent has control.

        :param environment: Collection of all the knowledge the Agent can access to in order to plan and move the arms.
        """
        self.environment = environment
        self.n_total_arms = self.environment.n_robotic_arms
        self.running_workers = []
        self.deployed_arms = 0
        self.active_mounting_points=[]

    def update_step(self):
        """
        Method that updates the step counter, ending a step t and starts the step t+1.
        """
        self.environment.update_time()
        self.n_total_arms = self.environment.n_robotic_arms

    def update_moved_arms(self):
        """
        Update the counter of total arms still not moved.
        """
        self.n_total_arms -= 1

    def all_arms_moved_in_current_step(self):
        """
        Method that checks if all the arms where moved at the current step, or not
        :return: Returns True if all the arms where moved, False otherwise.
        """
        if self.n_total_arms == 0:
            return True
        else:
            return False

    def deploy_arms(self, mode: str):
        if mode == "it" or mode == "iterative":
            self.deploy_arm()
        elif mode == "random" or mode == "rand" or mode == "rnd":
            self.random_deploy()

    def deploy_arm(self):
        """
        This method deploys the available arms over the available mounting points in an iterative way: the arms are
        deployed starting from the origin go the grid on all the available mounting points in order, based on the
        columns.
        """

        with alive_bar((self.environment.n_robotic_arms), bar="bubbles", dual_line=True,
                       title='Deploying Arms') as bar:
            for row in self.environment.districts:
                for district in row:
                    district.mounting_points.reverse()
                    district.sort_tasks()
                    for mounting_point_index, mouting_point in enumerate(district.mounting_points):
                        # print(district.ordered_tasks[mounting_point_index])
                        if not district.ordered_tasks[mounting_point_index]:  # if there are no task in district
                            continue
                        if self.deployed_arms < self.n_total_arms:
                            self.deployed_arms += 1
                            self.active_mounting_points.append((district, mounting_point_index))
                            bar(1)
        self.environment.draw(agent=self)

        # TODO: implement distance deployment strat

    def assign_tasks(self):
        with alive_bar(len(self.active_mounting_points), bar="bubbles", dual_line=True, title='Assigning Tasks') as bar:
            for keyValue in self.active_mounting_points:
                if len(keyValue[0].ordered_tasks[0]) > 0:
                    selectedTask = keyValue[0].ordered_tasks[keyValue[1]][0]
                    self.running_workers.append(
                    Worker.Worker(self.environment.add_robotic_arm(keyValue[0].mounting_points[keyValue[1]]), selectedTask,
                                  self.environment))
                    for ot in keyValue[0].ordered_tasks:
                        ot.remove(selectedTask)
                    self.environment.tasks.remove(selectedTask)
                    bar(1)

        # input()
        # time.sleep(sec_time)
    def compute_paths(self):
        create_graph_from_district(self)
        with alive_bar(len(self.running_workers), bar="bubbles", dual_line=True, title='Assigning Tasks') as bar:
            for worker in self.running_workers:
                id=global_coordinates_to_district_coordinates(worker.task.get_position,self.environment)
                target = worker.arm.graph.get_vertex(id)
                Dpath = [target.get_id]
                shortest(target,Dpath)
                worker.path=Dpath[::-1]
                bar(1)
    def print_paths(self):
        for index,worker in enumerate(self.running_workers):
            print("worker["+str(index)+"] path: ")
            print(worker.path)
    def random_deploy(self):
        """
        This method deploys the available arms over the available mounting points in a random way: a subset of mounting
        points is selected from all the available ones (without duplication) and the arms are deployed on this subset.
        The number of samples mounting points corresponds to the number of available arms.
        """
        randomMoutingPoints = random.sample(self.environment.mounting_points, self.environment.n_robotic_arms)
        for row in self.environment.districts:
            for district in row:
                district.sort_tasks()
        with alive_bar(self.environment.n_robotic_arms, bar="bubbles", dual_line=True,
                               title='Deploying Arms') as bar:

            for mountingpoint in randomMoutingPoints:
                currentDistrict = self.environment.calculate_district(mountingpoint.x, mountingpoint.y)
                mounting_point_index = currentDistrict.mounting_points.index(mountingpoint)
                self.active_mounting_points.append((currentDistrict, mounting_point_index))
                bar(1)
        self.deployed_arms = self.n_total_arms
        self.environment.draw(agent=self)

    def worker_move_arm(self, worker: Worker):
        """
        Method that moves the arm of the worker according to the plan.
        :param worker: The worker controlling the arm to move.
        """
        print("MOVE ARM")

    def run_assembly(self):
        """
        Method that applys all plans
        """
        print("ASSEBLING")

    def run_plan(self, planned_workers):
        """
        Executes the plans for the specific workers.
        :param planned_workers: Plan for the workers.
        """
        # TODO: imporve doc and merge with run assembly
        for worker in planned_workers:
            print(worker.plan)
        for current_step in range(self.environment.n_steps):
            print("[STEP]: " + str(current_step))
            for worker, planned_worker in zip(self.running_workers, planned_workers):
                try:
                    self.environment.move_robotic_arm(worker.arm, planned_worker.plan.pop(0))
                except IndexError:
                    input()
                    return
            self.environment.update_time()
            if drawFlag:
                self.environment.draw(agent=self)
        print("#######################")

        for worker in self.running_workers:
            print(worker.plan)