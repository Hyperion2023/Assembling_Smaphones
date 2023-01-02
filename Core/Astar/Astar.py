from queue import PriorityQueue
import heapq
from Core.Astar import State


def a_star(starting_state: State, goal_test: callable, g: callable, h: callable, max_state_evaluated: int = -1):
    """
    A star search algorithm implementation
    :param starting_state: the starting state of the search
    :param goal_test: function to perform goal test
    :param g: function to calculate the path cost
    :param h: function to calculate the heuristic
    :param max_state_evaluated: maximum number of state to be evaluated before halting the search
    :return: the goal state found by the A star algorithm or None if no goal state is found
    """
    best_state = starting_state
    fringe = PriorityQueue(0)
    # fringe = []
    starting_state.g = g(starting_state)
    starting_state.h = h(starting_state)
    starting_state.f = starting_state.g + starting_state.h
    fringe.put(starting_state)
    # heapq.heappush(fringe, starting_state)

    states_evaluated = 0
    while not fringe.empty():
        states_evaluated += 1
        current_state = fringe.get()
        if current_state.workers[0].task_points_done > best_state.workers[0].task_points_done:
            best_state = current_state
        if states_evaluated != -1 and states_evaluated > max_state_evaluated:
            return best_state, False
        # current_state = heapq.heappop(fringe)
        if states_evaluated % 50 == 0:
            print("f", current_state.f, end="\t")
            print("g: ", current_state.g, end="\t")
            print("h: ", current_state.h, end="\t")
            print("tpd: ", current_state.workers[0].task_points_done, end="\t")
            print("state evaluated", states_evaluated, end="\r")

        if goal_test(current_state):
            print("n of state evaluated: ", states_evaluated)
            return current_state, True
        for i, child in enumerate(current_state.get_children()):
            # print(i, end="\r")
            child.g = g(child)
            child.h = h(child)
            child.f = child.g + child.h
            # if child.f > current_state.f:
            #     continue
            fringe.put(child)
            # heapq.heappush(fringe, child)

