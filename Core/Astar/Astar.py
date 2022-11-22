from queue import PriorityQueue

from State import State


def a_star(starting_state: State, goal_test, g, h):
    fringe = PriorityQueue(0)
    fringe.put(g(starting_state) + h(starting_state), starting_state)

    while not fringe.empty():
        current_state = fringe.get()
        if goal_test(current_state):
            return current_state
        for child in current_state.get_children():
            fringe.put(g(child) + h(child), child)
    return None
