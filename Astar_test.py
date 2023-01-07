from Core import Agent
from Core.Utils.Data import create_Environment
import random
import pickle
path = r"Dataset/c_few_arms.txt"

random.seed(0)
env = create_Environment(path)
# env.draw()
boomer = Agent(env)
# boomer.environment.show()
# boomer.deploy_arms("rand")
# boomer.subdivide_in_districts(algorithm="hill_climbing", max_district_size=20, max_iter=100, alpha=3., n_restart=3)
boomer.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=200, max_iter=10000, alpha=0., initial_temperature=1000, n_restart=1)
boomer.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/2", max_time=5)
with open("./boomer.pickle", "wb") as f:
	pickle.dump(boomer, f)
with open("./boomer.pickle", "rb") as f:
	boomer = pickle.load(f)
# boomer.environment.n_steps = 10000
boomer.schedule_plans(max_iter=2000, max_time=600)
boomer.run_schedule()



# t = time.time()
# boomer.running_workers[0].plan_with_astar(None, a_star_max_trials=1000, retract_policy="7/8")
# t = time.time() - t
# print("plan generated in ", t, "seconds")
# print("plan is", len(boomer.running_workers[0].plan), "long")
# input()
# boomer.run_plan([boomer.running_workers[0]])
