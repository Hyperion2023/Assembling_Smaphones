from Core.Utils.Data import create_Environment
from Core.Agent import Agent
from Core.Astar.State import State
from Core.Astar.Astar import a_star
from Core.Astar.heuristic import *

if __name__ == "__main__":
    path = r"./Dataset/d_tight_schedule.txt"

    # state = State(None, 4)
    # state.get_children()

    env = create_Environment(path, district_size=4)
    # env.draw()
    boomer = Agent(env)
    # boomer.environment.show()
    boomer.deploy_arm()

    starting_state = State(env.matrix, boomer.running_workers)

    final_state = a_star(starting_state, goal_test, g, h)
    boomer.run_plan(final_state.workers)
    # boomer.running_workers[0].my_description()
    # boomer.run_assembly()
