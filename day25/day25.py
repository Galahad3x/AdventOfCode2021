def part1():
	trenches = []
	with open("easy.txt", "r") as f:
		for line in [ln.rstrip('\n') for ln in f.readlines()]:
			trenches.append([c for c in line])
	for tr in trenches:
		print(tr)
	print("___")
	step_c = 0
	steps = 1
	while steps != 0:
		steps = 0
		moved = []
		for i, trench in enumerate(trenches):
			for j, c in enumerate(trench):
				if str((i, j)) in moved:
					continue
				if c == ">":
					if trench[(j + 1) % len(trench)] == ".":
						trench[(j + 1) % len(trench)] = ">"
						trench[j] = "."
						moved.append(str((i, (j + 1) % len(trench))))
						steps += 1
		moved = []
		for i, trench in enumerate(trenches):
			for j, c in enumerate(trench):
				if str((i, j)) in moved:
					continue
				if c == "v":
					if trenches[(i + 1) % len(trenches)][j] == ".":
						trench[j] = "."
						trenches[(i + 1) % len(trenches)][j] = "v"
						moved.append(str(((i + 1) % len(trenches), j)))
						steps += 1
		print("After step", step_c, "there have been", steps, "moves")
		step_c += 1
		for tr in trenches:
			print("".join(tr))


if __name__ in "__main__":
	part1()
