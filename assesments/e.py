import time

from Core import Agent
from Core.Utils.Data import create_Environment
import pickle
path = r"Dataset/e_dense_workspace.txt"

env = create_Environment(path)
agent_e = Agent(env)
t = time.time()
agent_e.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=20, max_iter=10000, alpha=4., initial_temperature=100, n_restart=1)
time_subdivision = time.time() - t
with open("./agent_e.pickle", "wb") as f:
	pickle.dump(agent_e, f)
t = time.time()
agent_e.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/2", max_time=5)
agent_e.schedule_plans(max_iter=2000, max_time=600)
time_a_star = time.time() - t
# agent_e.run_schedule()

with open("./agent_e.pickle", "rb") as f:
	agent_e = pickle.load(f)
t = time.time()
agent_e.plan_all_workers(planning_alg="dijkstra")
agent_e.schedule_plans(max_iter=2000, max_time=600)
time_dijkstra = time.time() - t
# agent_e.run_schedule()
print("dijkstra", time_subdivision + time_dijkstra, "A*", time_subdivision + time_a_star)