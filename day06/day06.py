from tqdm import tqdm

def part1():
	with open("input.txt", "r") as f:
		fishes = [int(n) for n in f.readlines()[0].rstrip("\n").split(",")]
	print("Start " + str(0) + ": " + ",".join([str(n) for n in fishes]))
	for day in range(80):
		new_fish = []
		for i, _ in enumerate(fishes):
			fishes[i] -= 1
			if fishes[i] == -1:
				fishes[i] = 6
				new_fish.append(8)
		fishes.extend(new_fish)
	# print("Day " + str(day + 1) + ": " + ",".join([str(n) for n in fishes]))
	print(len(fishes))


def part2():
	fishes = {}
	with open("input.txt", "r") as f:
		fishes_file = [int(n) for n in f.readlines()[0].rstrip("\n").split(",")]
	for fish in fishes_file:
		try:
			fishes[fish] += 1
		except KeyError:
			fishes[fish] = 1
	# print("Start " + str(0) + ": " + ",".join([str(n) for n in fishes]))
	for day in tqdm(range(256)):
		new_fish = {6: 0}
		for fish_counter in fishes.keys():
			if fish_counter == 0:
				new_fish[6] += fishes[fish_counter]
				new_fish[8] = fishes[fish_counter]
			elif fish_counter == 7:
				new_fish[6] += fishes[fish_counter]
			else:
				new_fish[fish_counter - 1] = fishes[fish_counter]
		fishes = new_fish
		# print("Day " + str(day + 1) + ": " + ",".join([str(n) for n in fishes.values()]))
	print(sum(fishes.values()))
	print(26984457539)


if __name__ in "__main__":
	part2()
