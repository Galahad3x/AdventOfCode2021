import satsolver


def alo_amo():
	clauses = []
	alos = []
	for segment in range(7):
		alo = list(range((7 * segment) + 1, (7 * (segment + 1)) + 1))
		alos.append(alo)
		clauses.append(alo)
		for elem1 in alo:
			for elem2 in alo:
				if elem1 < elem2:
					clauses.append([-elem1, -elem2])
	for ind in range(7):
		elems = [alo[ind] for alo in alos]
		clauses.append(elems)
		for elem1 in elems:
			for elem2 in elems:
				if elem1 < elem2:
					clauses.append([-elem1, -elem2])
	return clauses


def letter(letter):
	return ord(letter) % ord("a")


def solve(solution, elem):
	positives = [s for s in solution if s > 0]
	positives.sort(key=abs)
	letters = {}
	for i, let in enumerate("abcdefg"):
		letters[let] = chr(((positives[i] - 1) % 7) + ord("a"))
	translated_elem = ""
	for letter in elem:
		for lt in letters.keys():
			if letters[lt] == letter:
				translated_elem += lt
	if len(translated_elem) == 2:
		return "1"
	elif len(translated_elem) == 3:
		return "7"
	elif len(translated_elem) == 4:
		return "4"
	elif len(translated_elem) == 5:
		if "e" in translated_elem:
			return "2"
		elif "b" in translated_elem:
			return "5"
		else:
			return "3"
	elif len(translated_elem) == 6:
		if "d" not in translated_elem:
			return "0"
		elif "c" not in translated_elem:
			return "6"
		else:
			return "9"
	else:
		return "8"


def part1():
	values = {}
	for j in range(10):
		values[j] = 0
	with open("easy.txt", "r") as f:
		patterns = []
		outputs = []
		for pattern, output in [ln.rstrip("\n").split("|") for ln in f.readlines()]:
			patterns.append([p for p in pattern.split(" ") if p != ""])
			outputs.append([p for p in output.split(" ") if p != ""])
	for i, pattern in enumerate(patterns):
		variables = 49
		clauses = alo_amo()
		# Find and add 1, 7 and 4
		five_lengths = []
		six_lengths = []
		for signal in pattern:
			# It's a 1
			if len(signal) == 2:
				# ALO and AMO for top segment
				clauses.append([letter(signal[0]) + 15, letter(signal[1]) + 15])
				clauses.append([-(letter(signal[0]) + 15), -(letter(signal[1]) + 15)])
				# ALO and AMO for bottom segment
				clauses.append([letter(signal[0]) + 36, letter(signal[1]) + 36])
				clauses.append([-(letter(signal[0]) + 36), -(letter(signal[1]) + 36)])
			elif len(signal) == 3:
				# It's a 7
				elems = [letter(e) for e in signal]
				clauses.append([v + 1 for v in elems])
				clauses.append([v + 15 for v in elems])
				clauses.append([v + 36 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Top segment
							clauses.append([-(elem1 + 1), -(elem2 + 1)])
							# Middle segment
							clauses.append([-(elem1 + 15), -(elem2 + 15)])
							# Bottom segment
							clauses.append([-(elem1 + 36), -(elem2 + 36)])
			elif len(signal) == 4:
				# It's a 4
				elems = [letter(e) for e in signal]
				clauses.append([v + 8 for v in elems])
				clauses.append([v + 15 for v in elems])
				clauses.append([v + 22 for v in elems])
				clauses.append([v + 36 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Left segment
							clauses.append([-(elem1 + 8), -(elem2 + 8)])
							# Right segment
							clauses.append([-(elem1 + 15), -(elem2 + 15)])
							# Middle segment
							clauses.append([-(elem1 + 22), -(elem2 + 22)])
							# Bottom segment
							clauses.append([-(elem1 + 36), -(elem2 + 36)])
			elif len(signal) == 5:
				five_lengths.append(signal)
				if len(five_lengths) < 3:
					continue
				# It's a 2, a 3 or a 5
				commons = [e for e in five_lengths[0] if e in five_lengths[1] and e in five_lengths[2]]
				elems = [letter(e) for e in commons]
				clauses.append([v + 1 for v in elems])
				clauses.append([v + 22 for v in elems])
				clauses.append([v + 43 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Top segment
							clauses.append([-(elem1 + 1), -(elem2 + 1)])
							# Middle segment
							clauses.append([-(elem1 + 22), -(elem2 + 22)])
							# Bottom segment
							clauses.append([-(elem1 + 43), -(elem2 + 43)])
			elif len(signal) == 6:
				# It's a 0, a 6 or a 9
				six_lengths.append(signal)
				if len(six_lengths) < 3:
					continue
				commons = [e for e in six_lengths[0] if e in six_lengths[1] and e in six_lengths[2]]
				elems = [letter(e) for e in commons]
				clauses.append([v + 1 for v in elems])
				clauses.append([v + 8 for v in elems])
				clauses.append([v + 36 for v in elems])
				clauses.append([v + 43 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Top segment
							clauses.append([-(elem1 + 1), -(elem2 + 1)])
							# Left segment
							clauses.append([-(elem1 + 8), -(elem2 + 8)])
							# Right segment
							clauses.append([-(elem1 + 36), -(elem2 + 36)])
							# Bottom segment
							clauses.append([-(elem1 + 43), -(elem2 + 43)])
		# solution = satsolver.main_from_list(clauses, variables)
		for elem in outputs[i]:
			if len(elem) == 2:
				values[1] += 1
			elif len(elem) == 3:
				values[7] += 1
			elif len(elem) == 4:
				values[4] += 1
			elif len(elem) == 7:
				values[8] += 1
	return values


def part2():
	values = {}
	for j in range(10):
		values[j] = 0
	with open("input.txt", "r") as f:
		patterns = []
		outputs = []
		for pattern, output in [ln.rstrip("\n").split("|") for ln in f.readlines()]:
			patterns.append([p for p in pattern.split(" ") if p != ""])
			outputs.append([p for p in output.split(" ") if p != ""])
	sols = []
	for i, pattern in enumerate(patterns):
		variables = 49
		clauses = alo_amo()
		# Find and add 1, 7 and 4
		five_lengths = []
		six_lengths = []
		for signal in pattern:
			# It's a 1
			if len(signal) == 2:
				# ALO and AMO for top segment
				clauses.append([letter(signal[0]) + 15, letter(signal[1]) + 15])
				clauses.append([-(letter(signal[0]) + 15), -(letter(signal[1]) + 15)])
				# ALO and AMO for bottom segment
				clauses.append([letter(signal[0]) + 36, letter(signal[1]) + 36])
				clauses.append([-(letter(signal[0]) + 36), -(letter(signal[1]) + 36)])
			elif len(signal) == 3:
				# It's a 7
				elems = [letter(e) for e in signal]
				clauses.append([v + 1 for v in elems])
				clauses.append([v + 15 for v in elems])
				clauses.append([v + 36 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Top segment
							clauses.append([-(elem1 + 1), -(elem2 + 1)])
							# Middle segment
							clauses.append([-(elem1 + 15), -(elem2 + 15)])
							# Bottom segment
							clauses.append([-(elem1 + 36), -(elem2 + 36)])
			elif len(signal) == 4:
				# It's a 4
				elems = [letter(e) for e in signal]
				clauses.append([v + 8 for v in elems])
				clauses.append([v + 15 for v in elems])
				clauses.append([v + 22 for v in elems])
				clauses.append([v + 36 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Left segment
							clauses.append([-(elem1 + 8), -(elem2 + 8)])
							# Right segment
							clauses.append([-(elem1 + 15), -(elem2 + 15)])
							# Middle segment
							clauses.append([-(elem1 + 22), -(elem2 + 22)])
							# Bottom segment
							clauses.append([-(elem1 + 36), -(elem2 + 36)])
			elif len(signal) == 5:
				five_lengths.append(signal)
				if len(five_lengths) < 3:
					continue
				# It's a 2, a 3 or a 5
				commons = [e for e in five_lengths[0] if e in five_lengths[1] and e in five_lengths[2]]
				elems = [letter(e) for e in commons]
				clauses.append([v + 1 for v in elems])
				clauses.append([v + 22 for v in elems])
				clauses.append([v + 43 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Top segment
							clauses.append([-(elem1 + 1), -(elem2 + 1)])
							# Middle segment
							clauses.append([-(elem1 + 22), -(elem2 + 22)])
							# Bottom segment
							clauses.append([-(elem1 + 43), -(elem2 + 43)])
			elif len(signal) == 6:
				# It's a 0, a 6 or a 9
				six_lengths.append(signal)
				if len(six_lengths) < 3:
					continue
				commons = [e for e in six_lengths[0] if e in six_lengths[1] and e in six_lengths[2]]
				elems = [letter(e) for e in commons]
				clauses.append([v + 1 for v in elems])
				clauses.append([v + 8 for v in elems])
				clauses.append([v + 36 for v in elems])
				clauses.append([v + 43 for v in elems])
				for elem1 in elems:
					for elem2 in elems:
						if elem1 < elem2:
							# Top segment
							clauses.append([-(elem1 + 1), -(elem2 + 1)])
							# Left segment
							clauses.append([-(elem1 + 8), -(elem2 + 8)])
							# Right segment
							clauses.append([-(elem1 + 36), -(elem2 + 36)])
							# Bottom segment
							clauses.append([-(elem1 + 43), -(elem2 + 43)])
		solution = satsolver.main_from_list(clauses, variables)
		sol = []
		for number in outputs[i]:
			sol.append(solve(solution, number))
		sols.append(int("".join(sol)))
	print(sols)
	print(sum(sols))


if __name__ in "__main__":
	# print(sum(part1().values()))
	part2()
