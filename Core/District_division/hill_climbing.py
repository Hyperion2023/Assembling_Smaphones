def hill_climbing(get_starting_state, max_iter, n_restart, policy="get_first"):
	best_state = None
	best_state_fitness = 0
	for restart in range(n_restart):
		print("RESTART", restart)
		current_state = get_starting_state()
		current_state_fitness = current_state.fitness()
		for n_iter in range(max_iter):
			print("n_iter:", n_iter, end=" ")
			print(current_state_fitness)
			best_child = None
			best_child_fitness = 0
			for child in current_state.get_children():
				child_fitness = child.fitness()
				if child_fitness > current_state_fitness:
					if policy == "get_first":
						current_state = child
						current_state_fitness = child_fitness
						break
					elif policy == "get_best":
						best_child = child
						best_child_fitness = child_fitness
			if policy == "get_first" and current_state != child:
				break
			if policy == "get_best":
				if best_child is None:
					break
				current_state = best_child
				current_state_fitness = best_child_fitness

		if current_state_fitness > best_state_fitness:
			best_state = current_state
			best_state_fitness = current_state_fitness

	return best_state
