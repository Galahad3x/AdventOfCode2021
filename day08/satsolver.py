#!/usr/bin/python
#######################################################################
# Code made by:
# Moises Bernaus Lechosa
# Marc Cervera Rosell
#######################################################################

# Libraries
import sys


# Classes

# First of all, we read the input file in this function and we take the data that we need.

def read_file(filename):
	clauses_list = []
	for line in open(filename):
		if line.startswith('c'):
			continue
		if line.startswith('p'):
			vars = line.split()[2]
			continue
		clause = [int(x) for x in line[:-2].split()]
		clauses_list.append(clause)
	return clauses_list, int(vars)


# If the clause it's not unitary, this function create a new clause with the unit changed.

def create_clause(formula, unit):
	list_of_clauses = []
	for c in formula:
		if unit in c:
			continue
		else:
			new_c = [var for var in c if var != -unit]
			# Falle aqui
			if not new_c:
				return -1
			list_of_clauses.append(new_c)
	return list_of_clauses


# We use the unit-propagation for simplify the set of the clauses.

def unit_propagation(formula):
	temp = []
	unit_clauses_list = [c for c in formula if len(c) == 1]
	while unit_clauses_list:
		unit = unit_clauses_list[0]
		formula = create_clause(formula, unit[0])
		temp += [unit[0]]
		if formula == -1:
			return formula, temp
		unit_clauses_list = [c for c in formula if len(c) == 1]
	return formula, temp


# This is the heuristic that we choose for solve the formula, this takes the shortest positive clause every
# iteration, comparing the last literal taken.

def shortest_clause(formula):
	best_lit = 0
	min_length = float('-inf')
	for c in formula:
		negative = sum(1 for lit in c if lit < 0)
		if not negative and len(c) < min_length:
			best_lit = c[0]
			min_length = len(c)
	if not best_lit:
		return formula[0][0]
	return best_lit


# We use the backtracking algorithm for solve the formula recursively using the previous function(with the heuristic
# of take the shortest positive clause). This is a DPLL algorithm.

def backtracking_algorithm(formula, k):
	formula, unit = unit_propagation(formula)
	if formula == -1:
		return False
	k = k + unit
	if not formula:
		return k
	var = shortest_clause(formula)
	sol = backtracking_algorithm(create_clause(formula, var), k + [var])
	if not sol:
		sol = backtracking_algorithm(create_clause(formula, -var), k + [-var])
	return sol


def main():
	clauses, vars = read_file(sys.argv[1])
	sol = backtracking_algorithm(clauses, [])
	print("c rober_sat")
	if sol:
		sol += [var for var in range(1, vars + 1) if var not in sol and -var not in sol]
		sol.sort(key=abs)
		print('s SATISFIABLE')
		print('v ' + ' '.join([str(x) for x in sol]) + ' 0')
	else:
		print('s UNSATISFIABLE')

def main_from_list(clauses, vars):
	sol = backtracking_algorithm(clauses, [])
	if sol:
		sol += [var for var in range(1, vars + 1) if var not in sol and -var not in sol]
		sol.sort(key=abs)
		return sol
	else:
		raise Exception("Unsatisfiable")


if __name__ == '__main__':
	main()
