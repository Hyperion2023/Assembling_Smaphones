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
boomer.running_workers[0].plan_with_astar(a_star_max_trials=1000, retract_policy="7/8")
t = time.time() - t
print("plan generated in ", t, "seconds")
print("plan is", len(boomer.running_workers[0].plan), "long")
input()
boomer.run_plan([boomer.running_workers[0]])
