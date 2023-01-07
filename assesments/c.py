import time

from Core import Agent
from Core.Utils.Data import create_Environment
import pickle
path = r"Dataset/c_few_arms.txt"

env = create_Environment(path)
agent_c = Agent(env)
t = time.time()
agent_c.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=120, max_iter=10000, alpha=1., initial_temperature=100, n_restart=1)
time_subdivision = time.time() - t
with open("./agent_c.pickle", "wb") as f:
	pickle.dump(agent_c, f)
t = time.time()
agent_c.plan_all_workers(planning_alg="astar", a_star_max_trials=1000, retract_policy="1/3", max_time=60)
agent_c.schedule_plans(max_iter=2000, max_time=600)
time_a_star = time.time() - t
print("A*", time_subdivision + time_a_star)
# agent_c.run_schedule()
exit(0)
with open("./agent_c.pickle", "rb") as f:
	agent_c = pickle.load(f)
t = time.time()
agent_c.plan_all_workers(planning_alg="dijkstra")
agent_c.schedule_plans(max_iter=2000, max_time=600)
time_dijkstra = time.time() - t
# agent_c.run_schedule()
print("dijkstra", time_subdivision + time_dijkstra, "A*", time_subdivision + time_a_star)