from tqdm import tqdm


class Cube:
	def __init__(self, command, x1, x2, y1, y2, z1, z2) -> None:
		self.command = command
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.z1 = z1
		self.z2 = z2

	def in_cube(self, x, y, z):
		if self.x1 <= x <= self.x2:
			if self.y1 <= y <= self.y2:
				if self.z1 <= z <= self.z2:
					return True
		return False

	def points(self):
		return (self.x1, self.y1, self.z1), (self.x1, self.y2, self.z1), (self.x1, self.y1, self.z2), (
			self.x1, self.y2, self.z2), (self.x2, self.y1, self.z1), (self.x2, self.y2, self.z1), (
			       self.x2, self.y1, self.z2), (self.x2, self.y2, self.z2)

	def volume(self):
		return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)


def part1():
	commands = []
	with open("input.txt", "r") as f:
		for com, line in [ln.rstrip('\n').split(" ") for ln in f.readlines()]:
			rangs = {}
			for rang in line.split(","):
				rangs[rang[0]] = (
					min([int(n) for n in rang[2:].split("..")]), max([int(n) for n in rang[2:].split("..")]) + 1)
			commands.append((com, rangs))
	on_cubes = 0
	cubes = []
	for command, ranges in tqdm(commands[::-1]):
		da_cube = Cube(command, ranges['x'][0], ranges['x'][1],
		               ranges['y'][0], ranges['y'][1],
		               ranges['z'][0], ranges['z'][1])
		if command == "on":
			total_mod = da_cube.volume()
			for cube in cubes:
				if cube.command == "on":
					if True in [cube.in_cube(x, y, z) for x, y, z in da_cube.points()]:
						for x in range(da_cube.x1, da_cube.x2):
							pass
		cubes.append(da_cube)
	print("Part 2:", on_cubes)


if __name__ in "__main__":
	part1()
