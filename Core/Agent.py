import math
import random
import statistics

from constraint import *
from Core import Worker, Environment
import types
if isinstance(Worker, types.ModuleType):
    Worker = Worker.Worker
from Core.District_division import ArmDeployment
from Core.District_division.genetic_algoritm import genetic_algorithm
from Core.District_division.hill_climbing import hill_climbing
from Core.District_division.simulated_annealing import simulated_annealing
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
        self.n_total_arms = self.environment.n_robotic_arms
        self.workers = []
        self.running_workers = []
        self.deployed_arms = 0
        self.active_mounting_points = []
        self.districts = None
        self.schedule = None
        self.planned = False

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
            print(worker.arm.moves)


    def subdivide_in_districts(self, algorithm: str = "genetic", max_iter=100, max_district_size=30, alpha=0.3, verbose=False, **kwargs):
        def get_starting_state():
            s = ArmDeployment(self.environment, max_district_size, alpha=alpha)
            s.random_init()
            return s

        if algorithm == "genetic":
            if "mutation_prob" in kwargs:
                mut_prob = kwargs["mutation_prob"]
            else:
                mut_prob = 0.3
            if "population_size" in kwargs:
                population_size = kwargs["population_size"]
            else:
                population_size = 20
            subdivision = genetic_algorithm(get_starting_state, population_size, mutation_probability=mut_prob, max_iter=max_iter, verbose=verbose)
        elif algorithm == "hill_climbing":
            if "n_restart" in kwargs:
                n_restart = kwargs["n_restart"]
            else:
                n_restart = 5
            if "policy" in kwargs:
                policy = kwargs["policy"]
            else:
                policy = "get_first"
            subdivision = hill_climbing(get_starting_state, max_iter, n_restart, policy)
        elif algorithm == "simulated_annealing":
            if "n_restart" in kwargs:
                n_restart = kwargs["n_restart"]
            else:
                n_restart = 5
            if "initial_temperature" in kwargs:
                initial_temperature = kwargs["initial_temperature"]
            else:
                initial_temperature = "get_first"
            subdivision = simulated_annealing(get_starting_state, max_iter, n_restart, initial_temperature)
        else:
            raise ValueError("algorithm not recognized")
        self.districts = subdivision.get_standard_districts()
        subdivision.draw_districts()
        print("total covered tasks:", subdivision.get_n_task_covered())

    def plan_all_workers(self, planning_alg="astar", **kwargs):
        if not self.districts:
            self.subdivide_in_districts()
        for d in self.districts:
            arm = self.environment.add_robotic_arm(d.mounting_points[0])
            for t in d.tasks:
                self.workers.append(Worker(arm, t, self.environment, district=d))
        for i, worker in enumerate(self.workers):
            print("worker", i)
            if planning_alg == "astar":
                if "a_star_max_trials" in kwargs:
                    a_star_max_trials = kwargs["a_star_max_trials"]
                else:
                    a_star_max_trials = 1000
                if "retract_policy" in kwargs:
                    retract_policy = kwargs["retract_policy"]
                else:
                    retract_policy = "1/2"
                worker.plan_with_astar(a_star_max_trials, retract_policy)
            # if planning_alg == "diskj---":
            #     worker.plan =

        self.workers = [worker for worker in self.workers if worker.plan is not None]
        self.planned = True

    def schedule_plans(self):
        # intersecting_zones = {}
        # for d1 in self.districts:
        #     intersecting_zones[d1] = {}
        #     for d2 in self.districts:
        #         if d1 == d2:
        #             continue
        #         inter = get_districts_intersection(d1, d2)
        #         if inter:
        #             intersecting_zones[d1][d2] = inter

        if not self.planned:
            self.plan_all_workers()

        worker_time = {}
        for worker in self.workers:
            worker_time[worker] = len(worker.plan)

        workers_shared_start = {}
        workers_shared_end = {}
        for worker in self.workers:
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

        class WorkerFlip:
            def __init__(self, w):
                self.w = w

            def __lt__(self, other):
                return str(self) < str(other)

        worker_flips = []
        average_value = statistics.mean([w.value for w in self.workers])
        for w in self.workers:
            worker_flip = WorkerFlip(w)
            problem.addVariable(w, list(range(0, self.environment.n_steps - len(w.plan), 5)))
            if w.value > average_value:
                problem.addVariable(worker_flip, [True])
            else:
                problem.addVariable(worker_flip, [True, False])
            worker_flips.append(worker_flip)
        # for w in self.workers:
        #     if len(w.plan) > 100:
        #         problem.addConstraint(lambda v: v < 10, (w,))
        #         break

        for w1, wf1 in zip(self.workers, worker_flips):
            for w2, wf2 in zip(self.workers, worker_flips):
                if w1 == w2:
                    continue
                if w1.district == w2.district:
                    problem.addConstraint(create_constraint_same_district(w1, w2, worker_time), (w1, w2, wf1, wf2))
                else:
                    if w2.district in workers_shared_start[w1] and w1.district in workers_shared_start[w2]:
                        problem.addConstraint(create_constraint_different_district(w1, w2, workers_shared_start, workers_shared_end), (w1, w2, wf1, wf2))

        self.schedule = problem.getSolutions()
        best_schedule = None
        best_score = 0
        for s in self.schedule:
            score = 0
            for var, val in s.items():
                if isinstance(var, WorkerFlip):
                    if val:
                        score += var.w.task.value
            if score > best_score:
                best_schedule = s
                best_score = score
        self.schedule = {}
        if best_schedule is not None:
            for var, val in best_schedule.items():
                if isinstance(var, WorkerFlip):
                    if val:
                        self.schedule[var.w] = best_schedule[var.w]

            min_time = min(*self.schedule.values())
            self.schedule = {w: t - min_time for w, t in self.schedule.items()}
            return self.schedule

    def run_schedule(self):
        if not self.schedule:
            self.schedule_plans()

        for t in range(self.environment.n_steps):
            for worker in self.workers:
                if self.schedule[worker] == t:
                    self.running_workers.append(worker)
                if worker in self.running_workers and self.schedule[worker] + len(worker.plan) == t:
                    self.running_workers.remove(worker)

            for worker in self.running_workers:
                if not self.environment.move_robotic_arm(worker.arm, worker.plan[t - self.schedule[worker]]):
                    raise Exception("Something in plan was wrong")

            self.environment.update_time()
            if drawFlag:
                self.environment.draw(agent=self)



# functions that create a lambda because python sucks and always do late binding
def create_constraint_same_district(w1, w2, worker_time):
    def f(v1, v2, vf1, vf2):
        if vf1 and vf2:
            return v1 + worker_time[w1] < v2 or v2 + worker_time[w2] < v1
        else:
            return True
    return f


def create_constraint_different_district(w1, w2, workers_shared_start, workers_shared_end):
    def f(v1, v2, vf1, vf2):
        if vf1 and vf2:
            return v1 + workers_shared_start[w1][w2.district] > \
                               v2 + workers_shared_end[w2][w1.district] or \
                               v1 + workers_shared_end[w1][w2.district] < \
                               v2 + workers_shared_start[w2][w1.district]
        else:
            return True
    return f
