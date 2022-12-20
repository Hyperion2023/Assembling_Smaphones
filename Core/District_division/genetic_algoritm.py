import random
import numpy as np


def get_weight_population_by_fitness(population: list, fitness_function) -> list:
	"""
	Computes for each configuration the probability to be selected (according to the fitness function)
	and returns the configurations (ordered in descending order)
	:param population: list of state that compose the population
	:param fitness_function: function to calculate the fitness score of a state
	:return: list of tuples, for each tuple the first element contains the state, while the second element
		corresponds to its fitness score
	"""
	# computing for each configuration the probability to be selected, according to the fitness function
	weighted_population = [
		(configuration, configuration_fitness)
		for (configuration, configuration_fitness) in zip(population, map(fitness_function, population))
	]

	# order by the fitness of configuration
	weighted_population.sort(key=lambda x: x[1], reverse=True)

	return weighted_population


def choose_parents_population(population: list, fitness_function) -> tuple:
	"""
	Choose 2 parents in the population. A member of the population probability to be picked is proportional to its
	value according to the fitness function.
	:param population: list, list of state
	:param fitness_function: function to calculate the fitness score of a state
	:return: tuple, a couple of randomly selected states weighted by their fitness value
	"""
	weighted_population = get_weight_population_by_fitness(population, fitness_function)

	# selected 2 parents with a probabity proportial to the configuration fitness
	configurations = []
	fitnesses = []
	for (configuration, configuration_fitness) in weighted_population:
		configurations.append(configuration)
		fitnesses.append(configuration_fitness)

	picked_parents = (random.choices(configurations, weights=fitnesses, k=2))

	return picked_parents[0], picked_parents[1]


def genetic_algorithm(
		population: list,
		fitness_function=None,
		reproduce=None,
		mutate=None,
		mutation_probability: float = None,
		max_iter: int = 1000,
		verbose: bool = False
) -> np.array:
	"""
	:param population: list, list of states to use as a starting points
	:param fitness_function: function, function used to evaluate the fitness of a state
	:param mutation_probability: float, probability of a random mutation. If not specified, a random
		probability is generated for every reproduction cycle
	:param max_iter: int, maximum number of iterations cycles
	:param verbose: bool
	:return: the best state in population, according to fitness
	"""
	if not fitness_function:
		fitness_function = lambda x: x.fitness()
	if not reproduce:
		reproduce = lambda x, y: x.reproduce(y)
	if not mutate:
		mutate = lambda x: x.mutate()

	for i in range(max_iter):  # iterate until some individual is fit enough, or enough time has elapsed
		if verbose:
			print(f"ITERATION {i}")

		new_population = []
		for _ in range(len(population)):
			# select randomly two individuals in the population, preferring these with better fitness
			parent1, parent2 = choose_parents_population(population, fitness_function)

			# let the parents reproduce
			child = reproduce(parent1, parent2)

			# do a mutation
			if random.random() < mutation_probability:
				child = mutate(child)

			# add new child to population
			new_population.append(child)

		population = new_population
		if verbose:
			fitness_values = get_weight_population_by_fitness(population, fitness_function)[0][1]
			fitness_mean = fitness_values / 1
			print("Mean fitness:", fitness_mean)

	# return best individual found according to fitness
	weighted_population = get_weight_population_by_fitness(population, fitness_function)
	print(weighted_population[0][1])
	print(weighted_population[1][1])
	return weighted_population[0][0]
