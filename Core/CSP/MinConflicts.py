import time

from alive_progress import alive_bar
from constraint import *
import random

class MinConflicts:
	def __init__(self):
		self.problem = Problem()
		self.variables = None
		self.domains = None
		self.constraints = None
		self.vconstraints = None
		self.assignment = {}

	def addVariable(self, variable, domain):
		self.problem.addVariable(variable, domain)

	def addConstraint(self, constraint, variables):
		self.problem.addConstraint(constraint, variables)

	def get_conflicts(self, var=None, only_n=False):
		n_conflict = 0
		conflicting_variables = set()

		if var:
			for constraint, variables in self.vconstraints[var]:
				if not constraint(variables, self.domains, self.assignment):
					n_conflict += 1
			return n_conflict, conflicting_variables

		for constraint, variables in self.constraints:
			if not constraint(variables, self.domains, self.assignment):
				n_conflict += 1
				if not only_n:
					for var in variables:
						conflicting_variables.add(var)
		return n_conflict, list(conflicting_variables)

	# def get_conflicting_variables(self):
	# 	conflicting_variables = []
	# 	for variable in self.variables:
	# 		for constraint, variables in self.vconstraints[variable]:
	# 			if not constraint(variables, self.domains, self.assignment):
	# 				conflicting_variables.append(variable)
	# 				break
	# 	return conflicting_variables
	#
	# def get_n_conflict(self):
	# 	n_conflict = 0
	# 	for constraint, variables in self.constraints:
	# 		if not constraint(variables, self.domains, self.assignment):
	# 			n_conflict += 1
	# 	return n_conflict

	def getSolution(self, max_iter, max_time):
		self.domains, self.constraints, self.vconstraints = self.problem._getArgs()
		self.variables = self.domains.keys()

		# good_solution = self.problem.getSolution()
		# if good_solution:
		# 	self.assignment = good_solution
		# 	return self.assignment

		for var in self.variables:
			self.assignment[var] = random.choice(self.domains[var])
		start_time = time.time()
		old_n_conflict = 10000000
		with alive_bar(max_iter, bar="bubbles", dual_line=True, title='Scheduling plans', force_tty=True) as bar:
			for n in range(max_iter):
				if time.time() - start_time > max_time:
					break

				n_conflict, conflicting_variables = self.get_conflicts()
				if n_conflict < old_n_conflict:
					print("conflicts:", n_conflict)
					old_n_conflict = n_conflict
				if n_conflict == 0:
					return self.assignment

				var_change = random.choice(conflicting_variables)

				# max_conflicts = 0
				# var_change = None
				# for var in self.variables:
				# 	v_conflict, _ = self.get_conflicts(var=var, only_n=True)
				# 	if v_conflict > max_conflicts:
				# 		max_conflicts = v_conflict
				# 		var_change = var

				best_value = self.assignment[var_change]
				best_v_conflict = 10000000
				for value in self.domains[var_change]:
					self.assignment[var_change] = value
					v_conflict, _ = self.get_conflicts(var=var_change, only_n=True)
					if v_conflict <= best_v_conflict:
						best_value = value
						best_v_conflict = v_conflict



				# if best_v_conflict == max_conflicts:
				# 	self.assignment[var_change] = best_value
				# 	var_change = random.choice(conflicting_variables)
				# 	best_value = self.assignment[var_change]
				# 	best_v_conflict = None
				# 	for value in self.domains[var_change]:
				# 		self.assignment[var_change] = value
				# 		v_conflict, _ = self.get_conflicts(var=var_change, only_n=True)
				# 		if not best_v_conflict or v_conflict <= best_v_conflict:
				# 			best_value = value
				# 			best_v_conflict = v_conflict

				self.assignment[var_change] = best_value
				bar(1)
