def opposite_move(m):
	if m == "R":
		return "L"
	if m == "L":
		return "R"
	if m == "U":
		return "D"
	if m == "D":
		return "U"
	if m == "W":
		return "W"
	raise ValueError("move not valid")
