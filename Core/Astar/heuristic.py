from Core.Utils.distances import manhattan_distance


def goal_test(state) -> bool:
    """
    Check if the state passed is a goal state (where all task point have been collected
    :param state: the state to check
    :return: True if the state is a goal state False otherwise
    """
    for worker in state.workers:
        if not worker.task_points_done == worker.task.n_points:
            return False
    return True


def g(state) -> int:
    return state.n_step


def h(state) -> int:
    """
    Calculate the heuristic value for the state passed, which is the max of the manhattan distances remaining
    to every arm to complete the task
    :param state: the state to calculate the heuristic on
    :return: the value of the heuristic
    """
    distances = [0 for _ in range(state.n_worker)]
    for i, worker in enumerate(state.workers):
        last_point = worker.arm.path[-1]
        for point in worker.task.points[worker.task_points_done:]:
            distances[i] += manhattan_distance(point, last_point)
            last_point = point
    return max(distances)
