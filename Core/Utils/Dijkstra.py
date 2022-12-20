import sys

import numpy

import Core


class Vertex:
    """
    Vertex class used to compute Dijkstra's shortest path algorithm.
    """
    def __init__(self, node: int):
        """
        Constructor for the Vertex class.
        :param node: ID of the vertex.
        """
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor: int, weight: int = 0):
        """
        Add a neighbor to the vertex.
        :param neighbor: ID of the neighbor.
        :param weight: Weight of the neighbor. (Default = 0)
        """
        self.adjacent[neighbor] = weight

    @property
    def get_connections(self):
        return self.adjacent.keys()

    @property
    def get_id(self):
        return self.id

    def get_weight(self, neighbor: int):
        return self.adjacent[neighbor]

    def set_distance(self, dist: int):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev: int):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __lt__(self, other: object):
        return self.distance < other.distance

    def __gt__(self, other: object):
        return self.distance > other.distance

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph:
    """
    Graph class used to compute Dijkstra's shortest path algorithm.
    """
    def __init__(self):
        """
        Constructor for the Graph class.
        """
        self.vert_dict = {}
        self.num_vertices = 0

    def create_graph_from_mat(self, matrix: numpy.matrix):
        """
        Create a graph from a matrix.
        :param matrix: Matrix to create the graph from.
        """
        cur_index = 0

        for row_index, row in enumerate(matrix):

            for col_index, col in enumerate(row):

                cur_index = row_index * len(row) + col_index
                if col_index != len(row) - 1:
                    test = self.get_vertex(cur_index)  # If im not in the dictionary
                    if not test:
                        self.add_vertex(cur_index)  # add me
                    test = self.get_vertex(cur_index + 1)
                    if not test:
                        self.add_vertex(cur_index + 1)
                    if not (matrix[row_index][col_index + 1] == (1, 0, 0)).all() and not (
                            matrix[row_index][col_index] == (1, 0, 0)).all():  # If im not a mounting point
                        self.add_edge(cur_index, cur_index + 1, 1)
                    else:
                        self.add_edge(cur_index, cur_index + 1, 1000000)

                if row_index != len(matrix) - 1:
                    test = self.get_vertex(cur_index)  # If im not in the dictionary
                    if not test:
                        self.add_vertex(cur_index)  # add me
                    test = self.get_vertex((row_index + 1) * len(row) + col_index)
                    if not test:
                        self.add_vertex((row_index + 1) * len(row) + col_index)
                    if not (matrix[row_index + 1][col_index] == (1, 0, 0)).all() and not (
                            matrix[row_index][col_index] == (1, 0, 0)).all():  # If im not a mounting point
                        # print("LINKING: "+str(cur_index)+" -> "+str((row_index+1)*len(row)+col_index))
                        self.add_edge(cur_index, (row_index + 1) * len(row) + col_index, 1)
                    else:
                        # print("LINKING: "+str(cur_index)+" -> "+str((row_index+1)*len(row)+col_index))
                        self.add_edge(cur_index, (row_index + 1) * len(row) + col_index, 1000000)




    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node: int):
        """
        Add a vertex to the graph.
        :param node: Node to add.
        """
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n: int):
        """
        Get a vertex from the graph.
        :param n: Node to get.
        """

        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm: int, to:int, cost:int=0):
        """
        Add an edge to the graph.
        :param frm: First node to add.
        :param to: Second node to add.
        :param cost: Cost of the edge.
        """
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        """
        Get all vertices in the graph.
        :return: List of vertices.
        """
        return self.vert_dict.keys()

    def set_previous(self, current):
        """
        Set the previous node in the graph.
        :param current: Previous node.
        """
        self.previous = current

    def get_previous(self, current):
        return self.previous


def shortest(v, path:int):
    """
    Get the shortest path from v to path.
    :param v: Source vertex.
    :param path: Destination vertex.
    :return: Path.
    """
    if v.previous:
        path.append(v.previous.get_id)
        shortest(v.previous, path)
    return


import heapq


def create_graph_from_district(environment:Core.Environment.Environment):
    """
    Generate a list of graphs for the districts in the environment.
    :param environment: Environment.
    :return: List of graphs.
    """
    list_of_graphs=[]
    for row in environment.districts:
        for district in row:
            # Each district has origin, w and h
            submatrix = environment.matrix[district.origin[0]:district.origin[0] + district.width,
                        district.origin[1]:district.origin[1] + district.height]
            g=Graph()
            g.create_graph_from_mat(submatrix)
            list_of_graphs.append(g)

    return list_of_graphs
def dijkstra(aGraph, start):
    """
    Given a Graph, compute Dijkstra's shortest path algorithm, given a starting vertex. This will generate the shortest
    path from start to all other vertices. With the function the shortest then any path starting in the start vertex can
    be easily computed.
    :param aGraph: Graph associated with a portion, or totality of the matrix.
    :param start: Starting vertex.
    """
    print("Dijkstra's shortest path")
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(
                    current)  # print("updated : current = "+str(current.get_id())+" next ="+str(next.get_id())+" new_dist = "+str( next.get_distance()))  # else:  #     print("not updated : current = "+str(current.get_id())+" next ="+str(next.get_id())+" new_dist = "+str( next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

# g = Graph()

# g.add_vertex('a')
# g.add_vertex('b')
# g.add_vertex('c')
# g.add_vertex('d')
# g.add_vertex('e')
# g.add_vertex('f')

# g.add_edge('a', 'b', 7)
# g.add_edge('a', 'c', 9)
# g.add_edge('a', 'f', 14)
# g.add_edge('b', 'c', 10)
# g.add_edge('b', 'd', 15)
# g.add_edge('c', 'd', 11)
# g.add_edge('c', 'f', 2)
# g.add_edge('d', 'e', 6)
# g.add_edge('e', 'f', 9)

# print("Graph data:")
# for v in g:
#     for w in v.get_connections():
#         vid = v.get_id()
#         wid = w.get_id()
#         print("( %s , %s, %3d)", ( vid, wid, v.get_weight(w)))

# dijkstra(g, g.get_vertex('a'), g.get_vertex('e'))

# target = g.get_vertex('e')
# path = [target.get_id()]
# shortest(target, path)
# print ("The shortest path : %s",(path[::-1]))
