import random

from constraint import *
from Core import Worker, Environment, RoboticArm, District
from alive_progress import alive_bar

from Core.District_division.ArmDeployment import ArmDeployment
from Core.Utils.conversion import global_coordinates_to_district_coordinates
from Core.Utils.districts import get_districts_intersection
from Core.District_division.genetic_algoritm import genetic_algorithm
from Core.Utils.Dijkstra import *
drawFlag = True
sec_time = 10



def get_times_in_shared_zone(worker, d):
    t0 = None
    t1 = None
    head = (worker.arm.mounting_point.x, worker.arm.mounting_point.y)
    path_in_shared_zone = [head]
    for i, move in enumerate(worker.plan):
        if move == "U":
            head = (head[0], head[1] + 1)
        elif move == "R":
            head = (head[0] + 1, head[1])
        elif move == "D":
            head = (head[0], head[1] - 1)
        elif move == "L":
            head = (head[0] - 1, head[1])

        if len(path_in_shared_zone) > 1:
            if head == path_in_shared_zone[-2]:
                path_in_shared_zone.pop()
            else:
                path_in_shared_zone.append(head)
        elif d.is_in(head):
            path_in_shared_zone.append(head)
            if t0 is None:
                t0 = i
            t1 = None

        if len(path_in_shared_zone) == 1:
            path_in_shared_zone = [head]
            if t1 is None:
                t1 = i

    return t0, t1

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
        # self.n_total_arms = self.environment.n_robotic_arms
        self.running_workers = []
        self.deployed_arms = 0
        self.active_mounting_points = []
        self.districts = None

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
                            self.active_mounting_points.append((district,mounting_point_index))
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


    def subdivide_in_districts(self, algorithm: str = "genetic", max_district_size=30, *args, **kwargs):
        if algorithm == "genetic":
            if "alpha" in kwargs:
                alpha = kwargs["alpha"]
            else:
                alpha = 0.1
            starting_population = [ArmDeployment(self.environment, max_district_size, alpha=alpha) for _ in range(20)]
            for s in starting_population:
                s.random_init()
            subdivision = genetic_algorithm(starting_population, mutation_probability=0.3, max_iter=100, verbose=True)
            self.districts = subdivision.get_standard_districts()

    def plan_all_workers(self, planning_alg="astar"):
        if not self.districts:
            self.subdivide_in_districts()
        for d in self.districts:
            arm = RoboticArm()
            arm.mount(d.mounting_point[0])
            for t in d.tasks:
                self.running_workers.append(Worker(arm, t, self.environment, district=d))
        for worker in self.running_workers:
            if planning_alg == "astar":
                # worker.plan_with_astar()
                worker.plan = ["U"]

    def schedule_plans(self):
        # self.plan_all_workers()
        # intersecting_zones = {}
        # for d1 in self.districts:
        #     intersecting_zones[d1] = {}
        #     for d2 in self.districts:
        #         if d1 == d2:
        #             continue
        #         inter = get_districts_intersection(d1, d2)
        #         if inter:
        #             intersecting_zones[d1][d2] = inter

        worker_time = {}
        for worker in self.running_workers:
            worker_time[worker] = len(worker.plan)

        workers_shared_start = {}
        workers_shared_end = {}
        for worker in self.running_workers:
            worker_shared_start = {}
            worker_shared_end = {}
            for d in self.districts:
                if d == worker.district:
                    continue
                t0, t1 = get_times_in_shared_zone(worker, d)
                if t0 is None:
                    continue
                worker_shared_start[d] = t0
                worker_shared_end[d] = t1
            workers_shared_start[worker] = worker_shared_start
            workers_shared_end[worker] = worker_shared_end

        problem = Problem()
        for w in self.running_workers:
            problem.addVariable(w, list(range(20 - len(w.plan))))

        for w1 in self.running_workers:
            for w2 in self.running_workers:
                if w1 == w2:
                    continue
                if w1.district == w2.district:
                    problem.addConstraint(create_constraint_same_district(w1, w2, worker_time), (w1, w2))
                else:
                    if w2.district in workers_shared_start[w1] and w1.district in workers_shared_start[w2]:
                        problem.addConstraint(create_constraint_different_district(w1, w2, workers_shared_start, workers_shared_end), (w1, w2))

        solution = problem.getSolution()
        return solution


# functions that create a lambda because python sucks and always do late binding
def create_constraint_same_district(w1, w2, worker_time):
    return lambda v1, v2: v1 + worker_time[w1] < v2 or v2 + worker_time[w2] < v1


def create_constraint_different_district(w1, w2, workers_shared_start, workers_shared_end):
    return lambda v1, v2: v1 + workers_shared_start[w1][w2.district] > \
                               v2 + workers_shared_end[w2][w1.district] or \
                               v1 + workers_shared_end[w1][w2.district] < \
                               v2 + workers_shared_start[w2][w1.district]

