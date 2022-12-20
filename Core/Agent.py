from Core import Worker, Environment
import random
import time

drawFlag = True
sec_time = 10


class Agent:
    """
    Class that represents the Agent responsbile of supervising all the workers in the environment.
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

    def deploy_arm(self):
        """
        This method deploys the available arms over the available mounting points in an iterative way: the arms are
        deployed starting from the origin go the grid on all the available mounting points in order, based on the
        columns.
        """

        for row in self.environment.districts:
            for district in row:
                district.mounting_points.reverse()
                district.sort_tasks()
                for mounting_point_index, mouting_point in enumerate(district.mounting_points):
                    # print(district.ordered_tasks[mounting_point_index])
                    if not district.ordered_tasks[mounting_point_index]:  # if there are no task in district
                        continue
                    selectedTask = district.ordered_tasks[mounting_point_index][0]
                    if self.deployed_arms < self.n_total_arms:
                        self.deployed_arms += 1
                        self.running_workers.append(
                            Worker(self.environment.add_robotic_arm(mouting_point), selectedTask,self.environment))
                        for ot in district.ordered_tasks:
                            ot.remove(selectedTask)
                        self.environment.tasks.remove(selectedTask)
        self.environment.draw(agent=self)

        # TODO: implement distance deployment strat

        # input()
        # time.sleep(sec_time)

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
        for mountingpoint in randomMoutingPoints:
            currentDistrict = self.environment.calculate_district(mountingpoint.x, mountingpoint.y)
            mounting_point_index = currentDistrict.mounting_points.index(mountingpoint)
            selectedTask = currentDistrict.ordered_tasks[mounting_point_index][0]
            self.running_workers.append(
                Worker(self.environment.add_robotic_arm(mountingpoint), selectedTask,self.environment))
            for ot in currentDistrict.ordered_tasks:
                ot.remove(selectedTask)
            self.environment.tasks.remove(selectedTask)
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
        #TODO: imporve doc and merge with run assembly
        for worker in planned_workers:
            print(worker.arm.moves)
        for current_step in range(self.environment.n_steps):
            print("[STEP]: " + str(current_step))
            for worker, planned_worker in zip(self.running_workers, planned_workers):
                try:
                    self.environment.move_robotic_arm(worker.arm, planned_worker.arm.moves.pop(0))
                except IndexError:
                    return
            self.environment.update_time()
            if drawFlag:
                self.environment.draw(agent=self)
        print("#######################")

        for worker in self.running_workers:
            print(worker.arm.moves)