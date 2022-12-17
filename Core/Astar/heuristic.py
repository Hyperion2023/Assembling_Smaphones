def goal_test(state):
    for worker in state.workers:
        if not worker.arm.task_points_done == worker.task.n_points:
            return False
    return True


def g(state):
    return state.n_step


def h(state):
    distances = [0 for _ in range(state.n_worker)]
    for i, worker in enumerate(state.workers):
        last_point = worker.arm.path[-1]
        for point in worker.task.points[worker.arm.task_points_done:]:
            distances[i] += manhattan_distance(point, last_point)
            last_point = point
    return max(distances)


def manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

