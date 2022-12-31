from Core.Utils.Data import create_Environment
# from .DisjoinedSubdivision import DisjoinedSubdivision
from Core.District_division.genetic_algoritm import *
from Core.District_division.ArmDeployment import ArmDeployment


path = r"./../../Dataset/d_tight_schedule.txt"

env = create_Environment(path)

# initial_population = [DisjoinedSubdivision(env, 4) for _ in range(20)]
# for s in initial_population:
# 	s.random_init()
#
# # super slow, need to find a faster way to get district from centers
# res = genetic_algorithm(initial_population, mutation_probability=0.3, max_iter=3, verbose=True)
# res.draw_districts()


initial_population = [ArmDeployment(env, 5, alpha=0.8) for _ in range(100)]
for s in initial_population:
	s.random_init()

res = genetic_algorithm(initial_population,  mutation_probability=0.5, max_iter=100, verbose=True)
print("task covered", res.get_n_task_covered())
print("task score", res.get_total_covered_score())
print("max_size", res.max_district_size)
res.draw_districts()
