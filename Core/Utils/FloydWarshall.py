import sys

from alive_progress import alive_bar


def get_floyd_warshall(district):
    graph = district.graph
    dist = {k: {} for k in graph.vert_dict.keys()}
    pred = {k: {} for k in graph.vert_dict.keys()}
    for l1, v1 in graph.vert_dict.items():
        for l2, v2 in graph.vert_dict.items():
            if v1 == v2:
                dist[l1][l2] = 0
            elif v2 in v1.adjacent.keys():
                dist[l1][l2] = v1.adjacent[v2]
            else:
                dist[l1][l2] = sys.maxsize
            pred[l1][l2] = l1

    with alive_bar(graph.num_vertices ** 3, bar="bubbles", dual_line=True, title='Floyd Warshall') as bar:
        for l1 in graph.vert_dict.keys():
            for l2 in graph.vert_dict.keys():
                for l3 in graph.vert_dict.keys():
                    if dist[l2][l3] > dist[l2][l1] + dist[l1][l3]:
                        dist[l2][l3] = dist[l2][l1] + dist[l1][l3]
                        pred[l2][l3] = pred[l1][l3]
                    bar(1)

    return dist, pred


