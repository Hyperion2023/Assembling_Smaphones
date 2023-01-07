import time

from Core import Agent
from Core.Utils.Data import create_Environment
import pickle
path = r"Dataset/d_tight_schedule.txt"

env = create_Environment(path)
agent_d = Agent(env)
t = time.time()
agent_d.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=20, max_iter=10000, alpha=3., initial_temperature=100, n_restart=1)
time_subdivision = time.time() - t
with open("./agent_d.pickle", "wb") as f:
	pickle.dump(agent_d, f)
t = time.time()
agent_d.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/2", max_time=5)
agent_d.schedule_plans(max_iter=2000, max_time=600)
time_a_star = time.time() - t
# agent_d.run_schedule()

with open("./agent_d.pickle", "rb") as f:
	agent_d = pickle.load(f)
t = time.time()
agent_d.plan_all_workers(planning_alg="dijkstra")
agent_d.schedule_plans(max_iter=2000, max_time=600)
time_dijkstra = time.time() - t
# agent_d.run_schedule()
print("dijkstra", time_subdivision + time_dijkstra, "A*", time_subdivision + time_a_star)