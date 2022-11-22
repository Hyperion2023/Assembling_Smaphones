import itertools

class State:
    def __init__(self, matrix, n_arms):
        self.matrix = matrix
        self.n_arms = n_arms
        self.n_step = 0

    # def is_move_valid(self,move):
        # not out of boundaries
        # not mouting point
        # not occupied by another arm or part of the same arm
        # check concurrent move to the same spot
        # retract control with previous move to avoid

    def get_children(self):
        move_set = [["U", "D", "L", "R", "W"] for _ in range(self.n_arms)]
        for move in itertools.product(*move_set):
            if move == tuple(["W" for _ in range(self.n_arms)]):
                continue
            if not self.is_move_valid(move):
                continue
            print(move)
            yield self.get_new_state(move)

    def get_new_state(self, move):
        new_state = State(self.matrix)
        # new_state =
