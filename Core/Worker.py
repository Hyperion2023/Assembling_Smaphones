from Core import Environment, RoboticArm, Task
from Core.Astar import State, a_star, goal_test, h, g
from Core.Planner.Path import OptimalPath
from copy import deepcopy

class Worker:
    """
    The Worker class that controls an arm.

    Attributes
    ----------
    arm : Core.RoboticArm.RoboticArm
        The robotic arm assigned to this worker.
    task : Core.Task.Task
        The task assigned to this arm.
    task_points_done: int
        The number of task points done.
    plan: list[tuple[int, int]]
        The plan of the arm to follow.
    action_taken: bool
        Whether the action was taken.
    env: Core.Environment.Environment
        The environment in which the worker is running.


    """
    def __init__(self, arm: RoboticArm, task: Task, env: Environment):
        """
        Worker Class, it takes and arm and a task and performs all the required step to complete the task.
        :param arm: Robotic Arm to cotrol
        :type arm: RoboticArm
        :param task: Task to perform
        :type task: Task
        :param env: Environment in which the arm moves
        :type env: Environment
        """
        self.arm = arm
        self.task = task
        self.task_points_done = 0
        self.plan = []  # TODO: implement in future version
        self.action_taken = False
        self.env = env
        #self.generate_optimal_path()

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

    def retract_n_steps(self, n):
        if n < 1:
            raise ValueError("retract must be at least 1 move")
        if n >= len(self.arm.path):
            raise ValueError("retract must be non superior to arm path lenght")
        r_move = "W"
        head_position = self.arm.path[-1]
        for i in range(n):
            new_head_position = self.arm.path[-(i + 2)]
            if new_head_position == (head_position[0], head_position[1] + 1):
                r_move = "U"
            if new_head_position == (head_position[0], head_position[1] - 1):
                r_move = "D"
            if new_head_position == (head_position[0] + 1, head_position[1]):
                r_move = "R"
            if new_head_position == (head_position[0] - 1, head_position[1]):
                r_move = "L"
            self.arm.moves.append(r_move)
            head_position = new_head_position
        self.arm.path = self.arm.path[:-n]

    def retract_all(self):
        self.retract_n_steps(len(self.arm.path) - 1)

    def retract(self):
        if not self.arm.collision_check:
            if len(self.arm.path) > 1:

                return True, self.arm.path[-2]
            else:

                return False, self.arm.path[-1]

        else:
            return False, (0, 0)  # TODO: to modify for real collision_check

    def plan_with_astar(self, a_star_max_trials):
        starting_state = State(self.env.matrix, [self])
        finished = False
        while not finished:
            final_state, finished = a_star(starting_state, goal_test, g, h, a_star_max_trials)
            # trial = 1
            # while not finished and trial < num_restarts:
            #     trial += 1
            #     final_state, finished = a_star(final_state, goal_test, g, h, a_star_max_trials)
            if not finished:

                # final_state.workers[0].retract_all()
                final_state.workers[0].retract_n_steps(3)
                # final_state.workers[0].retract_n_steps(int((len(final_state.workers[0].arm.path) - 1) / 5))
                starting_state = final_state

        self.plan = final_state.workers[0].arm.moves
    def __deepcopy__(self, memodict={}):
        w = Worker(deepcopy(self.arm, memodict), self.task, env=self.env)
        w.task_points_done = self.task_points_done
        return w
