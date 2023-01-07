import time

from Core import Agent
from Core.Utils.Data import create_Environment
import pickle
path = r"Dataset/f_decentralized.txt"

env = create_Environment(path)
agent_f = Agent(env)
t = time.time()
agent_f.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=80, max_iter=10000, alpha=3., initial_temperature=100, n_restart=1)
time_subdivision = time.time() - t
with open("./agent_f.pickle", "wb") as f:
	pickle.dump(agent_f, f)
t = time.time()
agent_f.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/2", max_time=5)
agent_f.schedule_plans(max_iter=2000, max_time=600)
time_a_star = time.time() - t
# agent_f.run_schedule()

with open("./agent_f.pickle", "rb") as f:
	agent_f = pickle.load(f)
t = time.time()
agent_f.plan_all_workers(planning_alg="dijkstra")
agent_f.schedule_plans(max_iter=2000, max_time=600)
time_dijkstra = time.time() - t
# agent_f.run_schedule()
print("dijkstra", time_subdivision + time_dijkstra, "A*", time_subdivision + time_a_star)