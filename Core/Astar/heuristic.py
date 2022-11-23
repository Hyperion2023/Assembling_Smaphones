def goal_test(state):
    for worker in state.workers:
        index = 0
        for point in worker.task.points:
            try:
                index = worker.arm.path.index(point, start=index)
            except ValueError:
                return False
    return True

def f(state):
    return state.n_step

def h(state):
    distances = []
    for worker in state.workers:
        index = 0
        for point in worker.task.points:
            try:
                index = worker.arm.path.index(point, start=index)
            except ValueError:
                return False
        print()