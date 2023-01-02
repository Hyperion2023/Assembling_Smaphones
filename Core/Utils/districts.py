from Core import District


def get_districts_intersection(d1, d2):
	leftX = max(d1.origin[0], d2.origin[0])
	rightX = min(d1.origin[0] + d1.width, d2.origin[0] + d2.width)
	bottomY = max(d1.origin[1], d2.origin[1])
	topY = min(d1.origin[1] + d1.height, d2.origin[1] + d2.height)

	if leftX < rightX and topY < bottomY:
		return District((leftX, bottomY), rightX - leftX, topY - bottomY)
	else:
		return None

