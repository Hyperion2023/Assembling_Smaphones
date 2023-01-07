from Core.Utils.Data import create_Environment
from genetic_algoritm import genetic_algorithm
from ArmDeployment import ArmDeployment
from simulated_annealing import simulated_annealing
from hill_climbing import hill_climbing
import pickle
import random
random.seed(0)
path = r"./../../Dataset/e_dense_workspace.txt"

env = create_Environment(path)

def get_random_starting_state():
	starting_state = ArmDeployment(env, 20, alpha=3.)
	starting_state.random_init()
	return starting_state

# res = hill_climbing(get_random_starting_state, 200, n_restart=1, policy="get_first")
# with open("./hill_climbing_sub.pickle", "wb") as f:
# 	pickle.dump(res, f)
# res.draw_districts()



res = simulated_annealing(get_random_starting_state, 10000, n_restart=1, initial_temperature=500)
print("entropy", res.get_entropy())
print("total_task_score", res.get_total_covered_score())
print("n_task", res.get_n_task_covered())
print("n_value", res.get_total_covered_value())
res.draw_districts()

# initial_population = [DisjoinedSubdivision(env, 4) for _ in range(20)]
# for s in initial_population:
# 	s.random_init()
#
# # super slow, need to find a faster way to get district from centers
# res = genetic_algorithm(initial_population, mutation_probability=0.3, max_iter=3, verbose=True)
# res.draw_districts()


# res = genetic_algorithm(get_random_starting_state, poplulation_size=50, mutation_probability=0.4, max_iter=100, verbose=True)
# print("task covered", res.get_n_task_covered())
# print("task score", res.get_total_covered_score())
# print("max_size", res.max_district_size)
# res.draw_districts()
