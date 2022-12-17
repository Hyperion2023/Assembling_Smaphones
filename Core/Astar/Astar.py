from queue import PriorityQueue
import heapq
from Core.Astar.State import State


def a_star(starting_state: State, goal_test, g, h, max_fringe_size=-1, fringe_size_tol=-1):
    fringe = PriorityQueue(0)
    # fringe = []
    starting_state.g = g(starting_state)
    starting_state.h = h(starting_state)
    starting_state.f = starting_state.g + starting_state.h
    fringe.put(starting_state)
    # heapq.heappush(fringe, starting_state)

    states_evaluated = 0
    while not fringe.empty():
    # while fringe:
    #     if max_fringe_size != -1 and fringe_size_tol != -1 and len(fringe) > max_fringe_size + fringe_size_tol:
    #         fringe = heapq.nsmallest(max_fringe_size, fringe)
    #         heapq.heapify(fringe)
        states_evaluated += 1
        current_state = fringe.get()
        # current_state = heapq.heappop(fringe)
        if states_evaluated % 50 == 0:
            print("\r")
            print("f", current_state.f, end="\t")
            print("g: ", current_state.g, end="\t")
            print("h: ", current_state.h, end="")
        if goal_test(current_state):
            print("n of state evaluated: ", states_evaluated)
            return current_state
        for i, child in enumerate(current_state.get_children()):
            # print(i, end="\r")
            child.g = g(child)
            child.h = h(child)
            child.f = child.g + child.h
            # if child.f == current_state.f:
            fringe.put(child)
            # heapq.heappush(fringe, child)
    return None
