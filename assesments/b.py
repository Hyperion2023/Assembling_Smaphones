import time

from Core import Agent
from Core.Utils.Data import create_Environment
import pickle
path = r"Dataset/b_single_arm.txt"

env = create_Environment(path)
agent_a = Agent(env)
t = time.time()
agent_a.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=100000, max_iter=100, alpha=0., initial_temperature=5, n_restart=1)
time_subdivision = time.time() - t
with open("./agent_a.pickle", "wb") as f:
	pickle.dump(agent_a, f)
t = time.time()
agent_a.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/2", max_time=5)
agent_a.schedule_plans(max_iter=2000, max_time=600)
time_a_star = time.time() - t
# agent_a.run_schedule()

with open("./agent_a.pickle", "rb") as f:
	agent_a = pickle.load(f)
t = time.time()
agent_a.plan_all_workers(planning_alg="dijkstra", a_star_max_trials=1000, retract_policy="1/2", max_time=5)
agent_a.schedule_plans(max_iter=2000, max_time=600)
time_dijkstra = time.time() - t
# agent_a.run_schedule()
print("dijkstra", time_subdivision + time_dijkstra, "A*", time_subdivision + time_a_star)