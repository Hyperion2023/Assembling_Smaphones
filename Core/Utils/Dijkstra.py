import multiprocessing
import sys
import heapq

import numpy
from alive_progress import alive_bar
from joblib import Parallel, delayed
from tqdm import tqdm

num_cores = multiprocessing.cpu_count()
from Core.Utils.conversion import *


class Vertex:
    """
    Vertex class used to compute Dijkstra's shortest path algorithm.

    Attributes
    ----------
    Id : int
        The id of the vertex.
    adjacent: dict
        A dictionary mapping each vertex to its adjacent vertices.
    distance : int
        The distance of the vertex. Initially infinite.
    visited : bool
        Whether the vertex has already been visited. Initially None.
    previous : Vertex
        The previous vertex.
    """

    def __init__(self, node):
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

    def add_neighbor(self, neighbor, weight: int = 1):
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

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_distance(self):
        return self.distance

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
        self.touched = False  # TO REMOVE; FOR DEBUG PURPOSES ONLY
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        """
        Add a vertex to the graph.
        :param node: Node to add.
        """
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        """
        Get a vertex from the graph.
        :param n: Node to get.
        """

        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost: int = 1):
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


def shortest(v, path: list):
    """
    Get the shortest path from v to path.
    :param v: Source vertex.
    :param path: Destination vertex.
    :return: Path.
    """
    #print("GETTING PATH")
    if v.previous:
        path.insert(0, v.previous.get_id)
        shortest(v.previous, path)

    return


def is_mounting_point(p, env):
    for m in env.mounting_points:
        if p == (m.x, m.y):
            return True
    return False


def create_district_graph_from_env(env, district):
    graph = Graph()
    for x in range(district.origin[0], district.origin[0] + district.width + 1, 1):
        for y in range(district.origin[1], district.origin[1] + district.height + 1, 1):
            if is_mounting_point((x, y), env) and (x, y) != (district.mounting_points[0].x, district.mounting_points[0].y):
                continue
            graph.add_vertex((x, y))  # add all the nodes that are not mounting points

    for x in range(district.origin[0], district.origin[0] + district.width + 1, 1):
        for y in range(district.origin[1], district.origin[1] + district.height + 1, 1):
            if is_mounting_point((x, y), env) and (x, y) != (district.mounting_points[0].x, district.mounting_points[0].y):
                continue
            if x + 1 <= district.origin[0] + district.width and (
                    not is_mounting_point((x + 1, y), env) or (x + 1, y) == (district.mounting_points[0].x, district.mounting_points[0].y)):
                graph.add_edge((x, y), (x + 1, y))
            if y + 1 <= district.origin[1] + district.height and (
                    not is_mounting_point((x, y + 1), env) or (x, y + 1) == (district.mounting_points[0].x, district.mounting_points[0].y)):
                graph.add_edge((x, y), (x, y + 1))
    return graph, graph.get_vertex((district.mounting_points[0].x, district.mounting_points[0].y))


def dijkstra(aGraph, start):
    """
    Given a Graph, compute Dijkstra's shortest path algorithm, given a starting vertex. This will generate the shortest
    path from start to all other vertices. With the function the shortest then any path starting in the start vertex can
    be easily computed.
    :param aGraph: Graph associated with a portion, or totality of the matrix.
    :param start: Starting vertex.
    """
    #print("Dijkstra's shortest path")
    # Set the distance for the start node to zero
    start.distance = 0
    aGraph.touched = True

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.visited = True

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.distance = new_dist
                next.previous = current
                # print("updated : current = "+str(current.get_id())+" next ="+str(next.get_id())+" new_dist = "+str( next.get_distance()))  # else:  #     print("not updated : current = "+str(current.get_id())+" next ="+str(next.get_id())+" new_dist = "+str( next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

    return aGraph
