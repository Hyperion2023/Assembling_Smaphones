from Core.Utils.Data import create_Environment
from Core.District_division import DisjoinedSubdivision
from Core.District_division.genetic_algoritm import genetic_algorithm
from Core.District_division import ArmDeployment
from Core.District_division.hill_climbing import hill_climbing
from Core.District_division.simulated_annealing import simulated_annealing


path = r"./../../Dataset/b_single_arm.txt"

env = create_Environment(path)

def get_random_starting_state():
	starting_state = ArmDeployment(env, 25, alpha=0.5)
	starting_state.random_init()
	return starting_state

# res = hill_climbing(get_random_starting_state, 200, n_restart=20, policy="get_best")
# res.draw_districts()

res = simulated_annealing(get_random_starting_state, 200, n_restart=1, initial_temperature=100)
res.draw_districts()

# initial_population = [DisjoinedSubdivision(env, 4) for _ in range(20)]
# for s in initial_population:
# 	s.random_init()
#
# # super slow, need to find a faster way to get district from centers
# res = genetic_algorithm(initial_population, mutation_probability=0.3, max_iter=3, verbose=True)
# res.draw_districts()


initial_population = [ArmDeployment(env, 25, alpha=0.5) for _ in range(20)]
for s in initial_population:
	s.random_init()

res = genetic_algorithm(initial_population,  mutation_probability=0.3, max_iter=100, verbose=True)
res.draw_districts()
