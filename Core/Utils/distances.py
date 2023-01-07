def manhattan_distance(p1: tuple, p2: tuple) -> int:
	"""
	Returns the Manhattan distance between two points.

	:param p1: First point.
	:param p2: Second point.
	:return: Manhattan distance between two points.
	"""
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def x_y_distance(p1: tuple, p2: tuple) -> tuple:
	"""
	Returns the x and y distance between two points.

	:param p1: First point.
	:param p2: Second point.
	:return: x and y distance between two points.
	"""
	return p2[0] - p1[0], p2[1] - p1[1]
