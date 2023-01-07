import random
import math


def simulated_annealing(get_starting_state, max_iter, n_restart, initial_temperature):
	best_state = None
	best_state_fitness = 0
	for restart in range(n_restart):
		print("RESTART", restart)
		current_state = get_starting_state()
		current_state_fitness = current_state.fitness()
		current_temperature = initial_temperature
		for n_iter in range(max_iter):
			print("n_iter:", n_iter, end=" ")
			print(current_state_fitness)

			child = next(current_state.get_children())
			child_fitness = child.fitness()
			delta_E = child_fitness - current_state_fitness
			if delta_E > 0 or (current_temperature > 0 and random.random() < math.exp(delta_E / current_temperature)):
				current_state = child
				current_state_fitness = child_fitness
			current_temperature -= 1

		if current_state_fitness > best_state_fitness:
			best_state = current_state
			best_state_fitness = current_state_fitness

	return best_state
