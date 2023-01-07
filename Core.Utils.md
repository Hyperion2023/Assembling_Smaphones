# Core.Utils package

## Submodules

## Core.Utils.Data module


### Core.Utils.Data.create_Environment(file_path, district_size=2)
Read the input file and create the environment. Generate several districts based on district_size.
:type file_path: `str`
:param file_path: Path to the input file.
:type district_size: `int`
:param district_size: Size of the districts.
:rtype: [`Environment`](Core.md#Core.Environment.Environment)
:return: Complete environment.

## Core.Utils.Dijkstra module


### _class_ Core.Utils.Dijkstra.Graph()
Bases: `object`

Graph class used to compute Dijkstra’s shortest path algorithm.


#### \__init__()
Constructor for the Graph class.


#### add_edge(frm, to, cost=0)
Add an edge to the graph.
:type frm: `int`
:param frm: First node to add.
:type to: `int`
:param to: Second node to add.
:type cost: `int`
:param cost: Cost of the edge.


#### add_vertex(node)
Add a vertex to the graph.
:type node: `int`
:param node: Node to add.


#### create_graph_from_mat(matrix)
Create a graph from a matrix.
:type matrix: `matrix`
:param matrix: Matrix to create the graph from.


#### get_previous(current)

#### get_vertex(n)
Get a vertex from the graph.
:type n: `int`
:param n: Node to get.


#### get_vertices()
Get all vertices in the graph.
:return: List of vertices.


#### set_previous(current)
Set the previous node in the graph.
:param current: Previous node.


### _class_ Core.Utils.Dijkstra.Vertex(node)
Bases: `object`

Vertex class used to compute Dijkstra’s shortest path algorithm.

### Attributes

Id

    The id of the vertex.

adjacent: dict

    A dictionary mapping each vertex to its adjacent vertices.

distance

    The distance of the vertex. Initially infinite.

visited

    Whether the vertex has already been visited. Initially None.

previous

    The previous vertex.


#### \__init__(node)
Constructor for the Vertex class.
:type node: `int`
:param node: ID of the vertex.


#### add_neighbor(neighbor, weight=0)
Add a neighbor to the vertex.
:type neighbor: `int`
:param neighbor: ID of the neighbor.
:type weight: `int`
:param weight: Weight of the neighbor. (Default = 0)


#### _property_ get_connections()

#### get_distance()

#### _property_ get_id()

#### get_weight(neighbor)

#### set_distance(dist)

#### set_previous(prev)

#### set_visited()

### Core.Utils.Dijkstra.create_graph_from_district(environment)
Generate a list of graphs for the districts in the environment.
:type environment: [`Environment`](Core.md#Core.Environment.Environment)
:param environment: Environment.
:return: List of graphs.


### Core.Utils.Dijkstra.dijkstra(aGraph, start)
Given a Graph, compute Dijkstra’s shortest path algorithm, given a starting vertex. This will generate the shortest
path from start to all other vertices. With the function the shortest then any path starting in the start vertex can
be easily computed.
:param aGraph: Graph associated with a portion, or totality of the matrix.
:param start: Starting vertex.


### Core.Utils.Dijkstra.shortest(v, path)
Get the shortest path from v to path.
:param v: Source vertex.
:type path: `int`
:param path: Destination vertex.
:return: Path.

## Core.Utils.conversion module


### Core.Utils.conversion.matrix_to_state(p)
Convert a matrix coordinates into a state vector.


* **Return type**

    `tuple`



### Core.Utils.conversion.state_to_matrix(p)
Convert a state vector into matrix coordinates.


* **Return type**

    `tuple`


## Core.Utils.distances module


### Core.Utils.distances.manhattan_distance(p1, p2)
Returns the Manhattan distance between two points.


* **Parameters**

    
    * **p1** (`tuple`) – First point.


    * **p2** (`tuple`) – Second point.



* **Return type**

    `int`



* **Returns**

    Manhattan distance between two points.



### Core.Utils.distances.x_y_distance(p1, p2)
Returns the x and y distance between two points.


* **Parameters**

    
    * **p1** (`tuple`) – First point.


    * **p2** (`tuple`) – Second point.



* **Return type**

    `tuple`



* **Returns**

    x and y distance between two points.


## Module contents
