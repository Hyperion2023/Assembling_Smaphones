def goal_test(state):
    for worker in state.workers:
        index = 0
        for point in worker.task.points:
            try:
                index = worker.arm.path.index(point, index)
            except ValueError:
                return False
    return True


def g(state):
    return state.n_step


def h(state):
    distances = [0 for _ in range(state.n_worker)]
    for i, worker in enumerate(state.workers):
        last_point = worker.arm.path[-1]
        index = 0
        for point in worker.task.points:
            try:
                index = worker.arm.path.index(point, index)
            except ValueError:
                distances[i] += manhattan_distance(point, last_point)
                last_point = point

    return max(distances)


def manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

