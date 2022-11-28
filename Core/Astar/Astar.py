from queue import PriorityQueue

from Core.Astar.State import State


def a_star(starting_state: State, goal_test, g, h):
    fringe = PriorityQueue(0)
    starting_state.g = g(starting_state)
    starting_state.h = h(starting_state)
    starting_state.f = starting_state.g + starting_state.h
    fringe.put(starting_state)

    states_evaluated = 0
    while not fringe.empty():
        states_evaluated += 1
        current_state = fringe.get()
        print("\r")
        print("f", current_state.f, end="\t")
        print("g: ", current_state.g, end="\t")
        print("h: ", current_state.h)
        if goal_test(current_state):
            print("n of state evaluated: ", states_evaluated)
            return current_state
        for i, child in enumerate(current_state.get_children()):
            print(i, end="\r")
            child.g = g(child)
            child.h = h(child)
            child.f = child.g + child.h
            fringe.put(child)
    return None
