from tqdm import tqdm

class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2) -> None:
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
        

def part1():
    commands = []
    with open("day22/input.txt", "r") as f:
        for com, line in [ln.rstrip('\n').split(" ") for ln in f.readlines()]:
            rangs = {}
            for rang in line.split(","):
                rangs[rang[0]] = (min([int(n) for n in rang[2:].split("..")]), max([int(n) for n in rang[2:].split("..")]) + 1)
            commands.append((com, rangs))
    on_cubes = 0
    cubes = []
    for command, ranges in tqdm(commands[::-1]):
        if command == "on":
            da_cube = Cube(ranges['x'][0], ranges['x'][1],
                            ranges['y'][0], ranges['y'][1],
                            ranges['z'][0], ranges['z'][1])
    print("Part 1:", on_cubes)



if __name__ in "__main__":
    part1()