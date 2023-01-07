from Core import District
import types
if isinstance(District, types.ModuleType):
	District = District.District

def get_districts_intersection(d1, d2):
	leftX = max(d1.origin[0], d2.origin[0])
	rightX = min(d1.origin[0] + d1.width, d2.origin[0] + d2.width)
	bottomY = max(d1.origin[1], d2.origin[1])
	topY = min(d1.origin[1] + d1.height, d2.origin[1] + d2.height)

	if leftX < rightX and bottomY < topY:
		return District((leftX, bottomY), rightX - leftX, topY - bottomY)
	else:
		return None

def recurrent_cluster(i, indexes, cluster, bbox):
    cluster.add(i)
    indexes[i] = True
    for j in list(map(lambda x: x[0], filter(lambda i: not i[1], indexes.items()))):

        # if box of index j has already been assigned skip
        if indexes[j]:
            continue

        if boxes_intersect(bbox[i], bbox[j]):
            recurrent_cluster(j, indexes, cluster, bbox)


def get_intersecting_clusters(bbox):
    clusters = []
    indexes = {i: False for i in range(len(bbox))}
    remaining = list(filter(lambda i: not i[1], indexes.items()))
    while remaining:
        cluster = set()
        remaining_i = remaining[0][0]
        recurrent_cluster(remaining_i, indexes, cluster, bbox)
        clusters.append(cluster)
        remaining = list(filter(lambda i: not i[1], indexes.items()))

    return clusters