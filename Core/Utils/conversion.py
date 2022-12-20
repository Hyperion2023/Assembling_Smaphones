def state_to_matrix(p: tuple) -> tuple:
    """
    Convert a state vector into matrix coordinates.
    """
    return p[1], p[0]


def matrix_to_state(p: tuple) -> tuple:
    """
    Convert a matrix coordinates into a state vector.
    """
    return p[1],  p[0]
