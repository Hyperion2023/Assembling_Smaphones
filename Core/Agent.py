import math
import random
import statistics
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

from constraint import *
from Core import Worker, Environment
import types

from Core.Utils.districts import get_districts_intersection

if isinstance(Worker, types.ModuleType):
    Worker = Worker.Worker
from Core.District_division import ArmDeployment
from Core.District_division.genetic_algoritm import genetic_algorithm
from Core.District_division.hill_climbing import hill_climbing
from Core.District_division.simulated_annealing import simulated_annealing
from Core.Utils.Dijkstra import *
from Core.CSP import MinConflicts
drawFlag = True
sec_time = 10


def plan_a_star(w, max_trials, rp):
    return w.plan_with_astar(max_trials, rp)


def get_times_in_shared_zone(worker, d):
    t0 = None
    t1 = None
    head = (worker.arm.mounting_point.x, worker.arm.mounting_point.y)
    if d.is_in(head):
        t0 = 0
        t1 = len(worker.plan) - 1
        return t0, t1
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

def are_path_intersecting(w1, w2):
    w1_cells = set()
    head = (w1.arm.mounting_point.x, w1.arm.mounting_point.y)
    w1_cells.add(head)
    for i, move in enumerate(w1.plan):
        if move == "U":
            head = (head[0], head[1] + 1)
        elif move == "R":
            head = (head[0] + 1, head[1])
        elif move == "D":
            head = (head[0], head[1] - 1)
        elif move == "L":
            head = (head[0] - 1, head[1])
        w1_cells.add(head)

    head = (w2.arm.mounting_point.x, w2.arm.mounting_point.y)
    for i, move in enumerate(w2.plan):
        if move == "U":
            head = (head[0], head[1] + 1)
        elif move == "R":
            head = (head[0] + 1, head[1])
        elif move == "D":
            head = (head[0], head[1] - 1)
        elif move == "L":
            head = (head[0] - 1, head[1])
        if head in w1_cells:
            return True

    return False

def recurrent_groups(i, indexes, group, district):
    group.add(i)
    indexes[i] = True
    for j in list(map(lambda x: x[0], filter(lambda i: not i[1], indexes.items()))):

        # if box of index j has already been assigned skip
        if indexes[j]:
            continue

        if get_districts_intersection(district[i], district[j]):
            recurrent_groups(j, indexes, group, district)


def get_intersecting_groups(districts):
    groups = []
    indexes = {i: False for i in range(len(districts))}
    remaining = list(filter(lambda i: not i[1], indexes.items()))
    while remaining:
        group = set()
        remaining_i = remaining[0][0]
        recurrent_groups(remaining_i, indexes, group, districts)
        groups.append(group)
        remaining = list(filter(lambda i: not i[1], indexes.items()))

    res = []
    for group in groups:
        if len(group) > 1:
            res.append([districts[d_index] for d_index in group])
    return res


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
        if planning_alg == "astar":
            if "a_star_max_trials" in kwargs:
                a_star_max_trials = kwargs["a_star_max_trials"]
            else:
                a_star_max_trials = 1000
            if "retract_policy" in kwargs:
                retract_policy = kwargs["retract_policy"]
            else:
                retract_policy = "1/2"
            if "max_time" in kwargs:
                max_time = kwargs["max_time"]
            else:
                max_time = "30"

        for d in self.districts:
            arm = self.environment.add_robotic_arm(d.mounting_points[0])
            for t in d.tasks:
                self.workers.append(Worker(arm, t, self.environment, district=d))

        # params = (self.workers, [a_star_max_trials for _ in self.workers], [retract_policy for _ in self.workers])
        #
        # with ProcessPoolExecutor() as executor:
        #     results = executor.map(plan_a_star, *params)
        results = []
        with alive_bar(len(self.workers), bar="bubbles", dual_line=True,
                       title='Planning paths', force_tty=True) as bar:
            for worker in self.workers:
                results.append(worker.plan_with_astar(a_star_max_trials, retract_policy, max_time))
                bar(1)

        self.workers = [worker for worker in results if worker.plan is not None and len(worker.plan) < self.environment.n_steps]
        print("Planned task:", len(self.workers))
        self.planned = True

    def schedule_plans(self, max_iter=1000, max_time=600):
        if not self.planned:
            self.plan_all_workers()

        intersecting_zones = {}
        for d1 in self.districts:
            intersecting_zones[d1] = {}
            for d2 in self.districts:
                if d1 == d2:
                    continue
                inter = get_districts_intersection(d1, d2)
                if inter:
                    intersecting_zones[d1][d2] = inter
                    d1.has_shared_region = True

        worker_time = {}
        for worker in self.workers:
            worker_time[worker] = len(worker.plan)
            if intersecting_zones[worker.district]:
                worker.simple_plan = False

        groups = get_intersecting_groups(self.districts)

        group_worker_dict = {i: [] for i in range(len(groups))}
        for index, districtList in enumerate(groups):
            for worker in self.workers:
                if worker.district in districtList:
                    group_worker_dict[index].append(worker)


        workers_shared_start = {}
        workers_shared_end = {}
        for worker in self.workers:
            if worker.simple_plan:
                continue
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

        # counter = 0
        # for worker in self.workers:
        #     if worker in workers_shared_start and workers_shared_start[worker] != {}:
        #         counter += 1
        # print("worker that enter in shared zone:", counter)

        self.schedule = {}
        for groups, workers in group_worker_dict.items():
            csp_min_conflict = MinConflicts()

            for w in workers:
                csp_min_conflict.addVariable(w, list(range(self.environment.n_steps - len(w.plan))))

            for i in range(len(workers)):
                w1 = workers[i]
                for w2 in workers[i+1:]:
                    if w1.district == w2.district:
                        csp_min_conflict.addConstraint(create_constraint_same_district(w1, w2, worker_time), (w1, w2))
                    else:
                        if w2.district in workers_shared_start[w1] and w1.district in workers_shared_start[w2] and are_path_intersecting(w1, w2):
                            csp_min_conflict.addConstraint(create_constraint_different_district(w1, w2, workers_shared_start, workers_shared_end), (w1, w2))

            print(f"solving a problem with {len(csp_min_conflict.problem._variables)} variables and {len(csp_min_conflict.problem._constraints)} constraints")
            csp_min_conflict.getSolution(max_iter, max_time)
            n_conflict, conflicting_variables = csp_min_conflict.get_conflicts()

            while n_conflict != 0:
                conflicting_variables.sort(key=lambda w: w.value)
                csp_min_conflict.assignment[conflicting_variables[0]] = -1
                csp_min_conflict.domains[conflicting_variables[0]].append(-1)
                n_conflict, conflicting_variables = csp_min_conflict.get_conflicts()

            schedule = csp_min_conflict.assignment

            min_time = min(*list(filter(lambda x: x > -1, schedule.values())))
            schedule = {w: t - min_time for w, t in schedule.items()}
            self.schedule.update(schedule)
        self.schedule_simple_worker()
        print("task scheduled: ", len(list(filter(lambda x: x > -1, self.schedule.values()))))
        total_score = 0
        for worker, t in self.schedule.items():
            if t > -1:
                total_score += worker.task.value
        print("total score achived: ", total_score)
        return self.schedule

    def schedule_simple_worker(self):
        district_worker = {d: [] for d in self.districts if d.has_shared_region == False}

        for w in self.workers:
            if w.simple_plan:
                district_worker[w.district].append(w)
        for d, worker_list in district_worker.items():
            worker_list.sort(key=lambda w: w.value, reverse=True)
            t = 0
            for w in worker_list:
                time = len(w.plan)
                if t+time > self.environment.n_steps:
                    self.schedule[w] = -1
                    continue
                self.schedule[w] = t
                t += time



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
    def f(v1, v2):
        if v1 != -1 and v2 != -1:
            return v1 + worker_time[w1] < v2 or v2 + worker_time[w2] < v1
        else:
            return True
    return f


def create_constraint_different_district(w1, w2, workers_shared_start, workers_shared_end):
    def f(v1, v2):
        if v1 != -1 and v2 != -1:
            return v1 + workers_shared_start[w1][w2.district] > \
                               v2 + workers_shared_end[w2][w1.district] or \
                               v1 + workers_shared_end[w1][w2.district] < \
                               v2 + workers_shared_start[w2][w1.district]
        else:
            return True
    return f
