# Core.Astar package

## Submodules

## Core.Astar.Astar module


### Core.Astar.Astar.a_star(starting_state, goal_test, g, h, max_fringe_size=-1, fringe_size_tol=-1)
A star search algorithm implementation
:type starting_state: `State`
:param starting_state: the starting state of the search
:type goal_test: `callable`
:param goal_test: function to perform goal test
:type g: `callable`
:param g: function to calculate the path cost
:type h: `callable`
:param h: function to calculate the heuristic
:type max_fringe_size: `int`
:param max_fringe_size:
:type fringe_size_tol: `int`
:param fringe_size_tol:
:return: the goal state found by the A star algorithm or None if no goal state is found

## Core.Astar.State module


### _class_ Core.Astar.State.State(matrix, workers, n_step=0)
Bases: `object`

Class that represent a state of the problem, consisting of the grid (immutable and shared between all states)
and the workers that are present in the problem


#### \__init__(matrix, workers, n_step=0)

#### check_boundaries(worker, move)
Chek if a move would make an arm head finish out of the grid.
:type worker: [`Worker`](Core.md#Core.Worker.Worker)
:param worker: the worker associated with the arm making the move
:type move: `str`
:param move: the move to be checked
:rtype: `tuple`
:return: a tuple containing True in the first element if the move can be done, False otherwise.
The second element is the new point where the head of the arm is after the move (if the move can be done).


#### get_children()
Yield al the possible state that can be obtained by the current state doing valid moves.


#### is_move_valid(moves)
Check if all the moves in the provided list (one for each worker) are valid, considering the boundaries of the grid,
the collision with other arms and the collision with mounting point.
:type moves: `tuple`
:param moves: the list of moves specified in the same order of the workers present in the state
:rtype: `tuple`
:return: a tuple containing True in the first element if all the moves can be done, False otherwise.
The second element is the new state generated from the current one after doing the moves.
If the moves are not valid return None.

## Core.Astar.heuristic module


### Core.Astar.heuristic.g(state)

* **Return type**

    `int`



### Core.Astar.heuristic.goal_test(state)
Check if the state passed is a goal state (where all task point have been collected
:type state: `State`
:param state: the state to check
:rtype: `bool`
:return: True if the state is a goal state False otherwise


### Core.Astar.heuristic.h(state)
Calculate the heuristic value for the state passed, which is the max of the manhattan distances remaining
to every arm to complete the task
:type state: `State`
:param state: the state to calculate the heuristic on
:rtype: `int`
:return: the value of the heuristic

## Module contents
