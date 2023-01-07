from Core import Agent
from Core.Utils.Data import create_Environment
import random
import pickle
from Core.Utils.FloydWarshall import create_graphs_from_districts, get_george_floyd
path = r"Dataset/c_few_arms.txt"

random.seed(0)
env = create_Environment(path)
boomer = Agent(env)
boomer.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=10000, max_iter=10000, alpha=10., initial_temperature=300, n_restart=1)
# create_graphs_from_districts(boomer)
# dist, pred = get_george_floyd(boomer.districts[0])
# dist2, pred2 = get_george_floyd(boomer.districts[1])
boomer.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/3", max_time=10)
# with open("./boomer.pickle", "wb") as f:
# 	pickle.dump(boomer, f)
# with open("./boomer.pickle", "rb") as f:
# 	boomer = pickle.load(f)
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
