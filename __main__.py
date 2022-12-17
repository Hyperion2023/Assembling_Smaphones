from Core.Utils.Data import create_Environment
from Core.Agent import Agent
from Core.Astar.State import State
from Core.Astar.Astar import a_star
from Core.Astar.heuristic import *
import time

if __name__ == "__main__":
    path = r"./Dataset/g_example.txt"

    # state = State(None, 4)
    # state.get_children()

    env = create_Environment(path, district_size=10)
    # env.draw()
    boomer = Agent(env)
    # boomer.environment.show()
    boomer.deploy_arm()

    starting_state = State(env.matrix, boomer.running_workers)

    t = time.time()
    final_state = a_star(starting_state, goal_test, g, h, 100, 100)
    t = time.time() - t
    print("time to planning:", t, "seconds")
    # t = list(final_state.get_children())
    boomer.run_plan(final_state.workers)
    # boomer.running_workers[0].my_description()
    # boomer.run_assembly()
    input()
