from Core.Utils.Data import create_Environment
from .DisjoinedSubdivision import DisjoinedSubdivision
from .genetic_algoritm import *
from .ArmDeployment import ArmDeployment


path = r"./../../Dataset/b_single_arm.txt"

env = create_Environment(path)

initial_population = [DisjoinedSubdivision(env, 4) for _ in range(20)]
for s in initial_population:
	s.random_init()

# super slow, need to find a faster way to get district from centers
res = genetic_algorithm(initial_population, mutation_probability=0.3, max_iter=3, verbose=True)
res.draw_districts()


initial_population = [ArmDeployment(env, 200, alpha=0.1) for _ in range(20)]
for s in initial_population:
	s.random_init()

res = genetic_algorithm(initial_population,  mutation_probability=0.3, max_iter=100, verbose=True)
res.draw_districts()
