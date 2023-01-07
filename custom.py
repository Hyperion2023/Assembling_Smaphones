import time

from Core import Agent
from Core.Utils.Data import create_Environment
import pickle
path = r"assesments/Dataset/cutsom_example.txt"

env = create_Environment(path)
agent_custom = Agent(env)
t = time.time()
agent_custom.subdivide_in_districts(algorithm="simulated_annealing", max_district_size=15, max_iter=1000, alpha=0.5, initial_temperature=100, n_restart=1)
time_subdivision = time.time() - t
with open("assesments/agent_custom.pickle", "wb") as f:
	pickle.dump(agent_custom, f)
t = time.time()
agent_custom.plan_all_workers(planning_alg="astar", a_star_max_trials=10000, retract_policy="1/2", max_time=60)
agent_custom.schedule_plans(max_iter=2000, max_time=600)
time_a_star = time.time() - t
input()
agent_custom.run_schedule()

with open("assesments/agent_custom.pickle", "rb") as f:
	agent_custom = pickle.load(f)
t = time.time()
agent_custom.plan_all_workers(planning_alg="dijkstra")
agent_custom.schedule_plans(max_iter=2000, max_time=600)
time_dijkstra = time.time() - t
input()
agent_custom.run_schedule()
print("dijkstra", time_subdivision + time_dijkstra, "A*", time_subdivision + time_a_star)