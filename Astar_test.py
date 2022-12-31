from Core import Agent
from Core.Astar import State, a_star, goal_test, g, h
from Core.Utils.Data import create_Environment
import time
path = r"Dataset/g_example.txt"

env = create_Environment(path, district_size=100)
# env.draw()
boomer = Agent(env)
# boomer.environment.show()
boomer.deploy_arms("rand")
boomer.assign_tasks()



t = time.time()
boomer.running_workers[0].plan_with_astar(10000)
t = time.time() - t
print("plan generated in ", t, "seconds")
input()
boomer.run_plan([boomer.running_workers[0]])
