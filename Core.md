# Core package

## Subpackages


* [Core.Astar package](Core.Astar.md)


    * [Submodules](Core.Astar.md#submodules)


    * [Core.Astar.Astar module](Core.Astar.md#module-Core.Astar.Astar)


        * [`a_star()`](Core.Astar.md#Core.Astar.Astar.a_star)


    * [Core.Astar.State module](Core.Astar.md#module-Core.Astar.State)


        * [`State`](Core.Astar.md#Core.Astar.State.State)


            * [`State.__init__()`](Core.Astar.md#Core.Astar.State.State.__init__)


            * [`State.check_boundaries()`](Core.Astar.md#Core.Astar.State.State.check_boundaries)


            * [`State.get_children()`](Core.Astar.md#Core.Astar.State.State.get_children)


            * [`State.is_move_valid()`](Core.Astar.md#Core.Astar.State.State.is_move_valid)


    * [Core.Astar.heuristic module](Core.Astar.md#module-Core.Astar.heuristic)


        * [`g()`](Core.Astar.md#Core.Astar.heuristic.g)


        * [`goal_test()`](Core.Astar.md#Core.Astar.heuristic.goal_test)


        * [`h()`](Core.Astar.md#Core.Astar.heuristic.h)


    * [Module contents](Core.Astar.md#module-Core.Astar)


* [Core.Planner package](Core.Planner.md)


    * [Submodules](Core.Planner.md#submodules)


    * [Core.Planner.LongTermPlanner module](Core.Planner.md#module-Core.Planner.LongTermPlanner)


    * [Core.Planner.Path module](Core.Planner.md#module-Core.Planner.Path)


        * [`OptimalPath`](Core.Planner.md#Core.Planner.Path.OptimalPath)


            * [`OptimalPath.__init__()`](Core.Planner.md#Core.Planner.Path.OptimalPath.__init__)


            * [`OptimalPath.compute_path()`](Core.Planner.md#Core.Planner.Path.OptimalPath.compute_path)


            * [`OptimalPath.valid_or_subpath()`](Core.Planner.md#Core.Planner.Path.OptimalPath.valid_or_subpath)


        * [`sign()`](Core.Planner.md#Core.Planner.Path.sign)


    * [Core.Planner.ShortTermPlanner module](Core.Planner.md#module-Core.Planner.ShortTermPlanner)


    * [Module contents](Core.Planner.md#module-Core.Planner)


* [Core.Utils package](Core.Utils.md)


    * [Submodules](Core.Utils.md#submodules)


    * [Core.Utils.Data module](Core.Utils.md#module-Core.Utils.Data)


        * [`create_Environment()`](Core.Utils.md#Core.Utils.Data.create_Environment)


    * [Core.Utils.Dijkstra module](Core.Utils.md#module-Core.Utils.Dijkstra)


        * [`Graph`](Core.Utils.md#Core.Utils.Dijkstra.Graph)


            * [`Graph.__init__()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.__init__)


            * [`Graph.add_edge()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.add_edge)


            * [`Graph.add_vertex()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.add_vertex)


            * [`Graph.create_graph_from_mat()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.create_graph_from_mat)


            * [`Graph.get_previous()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.get_previous)


            * [`Graph.get_vertex()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.get_vertex)


            * [`Graph.get_vertices()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.get_vertices)


            * [`Graph.set_previous()`](Core.Utils.md#Core.Utils.Dijkstra.Graph.set_previous)


        * [`Vertex`](Core.Utils.md#Core.Utils.Dijkstra.Vertex)


            * [`Vertex.__init__()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.__init__)


            * [`Vertex.add_neighbor()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.add_neighbor)


            * [`Vertex.get_connections`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.get_connections)


            * [`Vertex.get_distance()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.get_distance)


            * [`Vertex.get_id`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.get_id)


            * [`Vertex.get_weight()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.get_weight)


            * [`Vertex.set_distance()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.set_distance)


            * [`Vertex.set_previous()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.set_previous)


            * [`Vertex.set_visited()`](Core.Utils.md#Core.Utils.Dijkstra.Vertex.set_visited)


        * [`create_graph_from_district()`](Core.Utils.md#Core.Utils.Dijkstra.create_graph_from_district)


        * [`dijkstra()`](Core.Utils.md#Core.Utils.Dijkstra.dijkstra)


        * [`shortest()`](Core.Utils.md#Core.Utils.Dijkstra.shortest)


    * [Core.Utils.conversion module](Core.Utils.md#module-Core.Utils.conversion)


        * [`matrix_to_state()`](Core.Utils.md#Core.Utils.conversion.matrix_to_state)


        * [`state_to_matrix()`](Core.Utils.md#Core.Utils.conversion.state_to_matrix)


    * [Core.Utils.distances module](Core.Utils.md#module-Core.Utils.distances)


        * [`manhattan_distance()`](Core.Utils.md#Core.Utils.distances.manhattan_distance)


        * [`x_y_distance()`](Core.Utils.md#Core.Utils.distances.x_y_distance)


    * [Module contents](Core.Utils.md#module-Core.Utils)


## Submodules

## Core.Agent module


### _class_ Core.Agent.Agent(environment)
Bases: `object`

Class that represents the Agent responsible for supervising all the workers in the environment.

### Attributes

environment

    Environment object that represents the current state of the environment.

n_total_arms

    Total number of arms in the environment.

running_workers

    List of workers that are currently running.

deployed_arms: int

    Total number of arms deployed in the environment.


#### \__init__(environment)
Agent Class constructor. It imports the environment in which the agent has control.


* **Parameters**

    **environment** (*<module 'Core.Environment' from '/home/g752vsk/Documents/Assembling_Smaphones/Core/Environment.py'>*) – Collection of all the knowledge the Agent can access to in order to plan and move the arms.



#### all_arms_moved_in_current_step()
Method that checks if all the arms where moved at the current step, or not
:return: Returns True if all the arms where moved, False otherwise.


#### deploy_arm()
This method deploys the available arms over the available mounting points in an iterative way: the arms are
deployed starting from the origin go the grid on all the available mounting points in order, based on the
columns.


#### random_deploy()
This method deploys the available arms over the available mounting points in a random way: a subset of mounting
points is selected from all the available ones (without duplication) and the arms are deployed on this subset.
The number of samples mounting points corresponds to the number of available arms.


#### run_assembly()
Method that applys all plans


#### run_plan(planned_workers)
Executes the plans for the specific workers.
:param planned_workers: Plan for the workers.


#### update_moved_arms()
Update the counter of total arms still not moved.


#### update_step()
Method that updates the step counter, ending a step t and starts the step t+1.


#### worker_move_arm(worker)
Method that moves the arm of the worker according to the plan.
:type worker: <module ‘Core.Worker’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/Worker.py’>
:param worker: The worker controlling the arm to move.

## Core.District module


### _class_ Core.District.District(origin, width, height)
Bases: `object`

District class. A district is a spatial subdivision of the original matrix.

### Attributes

origin

    The origin of the district.

width

    The width of the district.

height

    The height of the district.

tasks

    The tasks in the district.

mounting_points

    The mounting points in the district.

robotic_arms

    The robotic arms in the district.

ordered_tasks

    The ordered tasks in the district for each arm.


#### \__init__(origin, width, height)
Constructor of the District class.
:type origin: `tuple`
:param origin: Tuple of points that indicate the bottom left point of the district area.
:type width: `int`
:param width: Integer that indicates how wide the district is.
:type height: `int`
:param height: Integer that indicates how high the district is.


#### add_mounting_point(mounting_point)
Method to add a mounting point that is contained in the district.
:type mounting_point: <module ‘Core.MountingPoint’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/MountingPoint.py’>
:param mounting_point: A mounting point that is contained in the district.


#### add_robotic_arm(robotic_arm)
Method to add a robotic arm that is contained in the district.
:type robotic_arm: <module ‘Core.RoboticArm’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/RoboticArm.py’>
:param robotic_arm: A robotic arm that is mounted on a mounting point in the district.


#### add_task(task)
Method to add the tasks contained in the district
:type task: <module ‘Core.Task’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/Task.py’>
:param task: A task in the district.


#### sort_tasks()
This methods generates a list of lists in which for each mounting point in the district, the tasks in the
district are sorted considering the best profitable way to complete them considering the distance and the total
points each tasks awards, starting form a given mounting point.

## Core.Environment module


### _class_ Core.Environment.Environment(width, height, n_steps, n_robotic_arms, district_size=17)
Bases: `object`

Class which contains all the information about the environment.


#### \__init__(width, height, n_steps, n_robotic_arms, district_size=17)
Constructor of the Environment Object. It receives the information from the given txt file configuration and
adapts it in order to let the Agent generate the plans for the robotic arms.
The origin of the working area is in the bottom left.
:type width: `int`
:param width: Width of the working space.
:type height: `int`
:param height: Height og the working space.
:type n_steps: `int`
:param n_steps: Max number of steps allowed to perform the moves.
:type n_robotic_arms: `int`
:param n_robotic_arms: Maximum number of deployable arms.
:type district_size: `int`
:param district_size: District height and width. (Default: 17)


#### add_mounting_points(mounting_points)
Adds the mounting points to the grid and adds them to the realtive district.
:type mounting_points: `list`
:param mounting_points: List of the x and y coordinates of the mounting points.


#### add_robotic_arm(mounting_point)
Mounts a robotic arm over a given mounting point.
:type mounting_point: <module ‘Core.MountingPoint’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/MountingPoint.py’>
:param mounting_point: Mouting point Object.
:rtype: <module ‘Core.RoboticArm’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/RoboticArm.py’>
:return: Arm object.


#### add_tasks(tasks, task_positions)
The method adds the tasks to the tasks list and sets marks on the grids the different subtasks points.
:type tasks: `list`
:param tasks: List of tasks to be added.
:type task_positions: `list`
:param task_positions: List of coordinates for each task.


#### calculate_district(x, y)
Given the x and y coordinates of a point, returns the district in which it is located.
:type x: `int`
:param x: X coordinate.
:type y: `int`
:param y: Y coordinate.
:rtype: <module ‘Core.District’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/District.py’>
:return: District in which the point is located.


#### draw(agent=None)
Method that draws a grid and is updated at each step to show how the environment evolves.
:param agent: If the method is called with agent != None it also draws the path of the agent.


#### is_move_valid(robotic_arm, action)
Method that checks if a move is valid and if it is the case, returns the point after the movement.
:type robotic_arm: <module ‘Core.RoboticArm’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/RoboticArm.py’>
:param robotic_arm: Robotic Arm to move.
:type action: `str`
:param action: Action to take
:rtype: `tuple`
:return: If the move can be taken it returns [True,new_point], otherwise [False,(0,0)]


#### move_robotic_arm(robotic_arm, action)
Method that checks if the given action is valid and if it is the case it performs a movement.
:type robotic_arm: <module ‘Core.RoboticArm’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/RoboticArm.py’>
:param robotic_arm: Robotic arm to move.
:type action: `str`
:param action: Action to take.
:rtype: `bool`
:return: True if the action has been take, False if the arm can’t make that action


#### show()
Method that lists all the visibile elements of the environment.


#### update_time()
Method that increments the given time by one step. If called and some robotic arms did not move, it appends to
their movements a Wait move.

## Core.MountingPoint module


### _class_ Core.MountingPoint.MountingPoint(x, y)
Bases: `object`

Mounting point class. It stores the x and y coordinates of a mounting point.

### Attributes

x

    X coordinate of the mounting point.

y

    Y coordinate of the mounting point.


#### \__init__(x, y)
Constructor of the class Mounting Point.
:type x: `int`
:param x: X coordinate.
:type y: `int`
:param y: Y coordinate.

## Core.RoboticArm module


### _class_ Core.RoboticArm.RoboticArm()
Bases: `object`

Class that represents a Robotic arm. It can mount it and check if the action si valid.
…
Attributes
———-
mounting_point : Core.MountingPoint.MountingPoint

> Mounting point of the arm.

path

    Path of the arm.

moves

    Set of moves performed on the arm.

collision_check

    Check if the arm is collision free.

graph

    Dijkstra graph from the mounting point.


#### \__init__()
Constructor of the RoboticArm class.


#### get_position()

#### mount(mounting_point)
Method that mounts an arm on a mounting point.
:type mounting_point: <module ‘Core.MountingPoint’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/MountingPoint.py’>
:param mounting_point: Mouting Point.

## Core.Task module


### _class_ Core.Task.Task(value=0, n_points=0)
Bases: `object`

Class tha represents a Task and contains it value and the positions of its points.

### Attributes

value

    The value of the task.

n_points

    The number of points in the task.

points

    The coordinates of the points of the task.

distance

    The distance between the points of the task.

score

    The score of the task with respect to the considered starting point.


#### \__init__(value=0, n_points=0)
Constructor of the class Task.
:type value: `int`
:param value: Value gained from completing the task. (Default: 0)
:type n_points: `int`
:param n_points: Number of sub-points required to visit in order to complete the task. (Default :0)


#### add_point(x, y)
Adds a tuple of coordinates in the correct order to the list of points to visit in order to complete the task.
:type x: `int`
:param x: X coordinate.
:type y: `int`
:param y: Y coordinate.


#### get_distance_between_two_points(index1, index2)
Mehtod that computes the distance between two points
:type index1: `tuple`
:param index1: First point.
:type index2: `tuple`
:param index2: Second point.
:rtype: `int`
:return: Distance between the two points.


#### get_distance_to_all_points(starting_position)
Computes the distances between a given point and all the points of the tasks.
In particular, it computes the distance between the starting_position and the first point, and the form the first
point to the second, and so on until the last one. All these distances are then appended and returned in a list
:type starting_position: `tuple`
:param starting_position: X,Y coordinate of the starting point.
:rtype: `list`
:return: List of distances


#### get_distance_to_first_point(position)
Method that computes the distance between the point given in input and the first point in the point list.
:type position: `tuple`
:param position: x,y coordinates of a point.
:rtype: `int`
:return: Distance.


#### _property_ get_position()
get the position of the first point.


#### get_task_score(mounting_point)
Method that computes a metric to sort the different tasks for each mounting point.
Given the total distance wrt the mounitng point position and the value of the task once completed, it computes
and return a score.
:type mounting_point: <module ‘Core.MountingPoint’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/MountingPoint.py’>
:param mounting_point: Mounting Point.
:rtype: `float`
:return: Score value.


#### _property_ show_task()
Print all the task points.


#### task_completed()
Method that checks if a task is/has been completed.
:rtype: `bool`
:return: True if the task is completed, orhterwise False.


#### task_target_update()
Method that removes the first point in the points list and decreases the number of total point to cover of the
given task.


#### update_distance(x, y)
Method that computes the distance between a given point and the first point of the tasks and then adds all the
distances between two consecutive points in the points list. This gives a metric of the minimum total distance
that and arm needs to cover in order to complete the task.
:param x: X point coordinate.
:param y: Y point coordinate.
:return: If there are no points in the list the function returns nothing.

## Core.Worker module


### _class_ Core.Worker.Worker(arm, task, env)
Bases: `object`

The Worker class that controls an arm.

### Attributes

arm

    The robotic arm assigned to this worker.

task

    The task assigned to this arm.

task_points_done: int

    The number of task points done.

plan: list[tuple[int, int]]

    The plan of the arm to follow.

action_taken: bool

    Whether the action was taken.

env: Core.Environment.Environment

    The environment in which the worker is running.


#### \__init__(arm, task, env)
Worker Class, it takes and arm and a task and performs all the required step to complete the task.
:type arm: <module ‘Core.RoboticArm’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/RoboticArm.py’>
:param arm: Robotic Arm to cotrol
:type arm: RoboticArm
:type task: <module ‘Core.Task’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/Task.py’>
:param task: Task to perform
:type task: Task
:type env: <module ‘Core.Environment’ from ‘/home/g752vsk/Documents/Assembling_Smaphones/Core/Environment.py’>
:param env: Environment in which the arm moves
:type env: Environment


#### generate_optimal_path()

#### my_description()

#### reset_action_taken()

#### retract()

#### take_action()
## Module contents

Core Package,
