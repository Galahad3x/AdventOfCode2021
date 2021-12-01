
def part1():
    increases = 0
    with open("day01/input.txt", "r") as f:
        previous = -1
        for depth in [int(d.rstrip(" ")) for d in f.readlines()]:
            if previous == -1:
                previous = depth
            else:
                if depth > previous:
                    increases += 1
                previous = depth
    print(increases)

def part2():
    increases = 0
    depths = []
    with open("day01/input.txt", "r") as f:
        for depth in [int(d.rstrip(" ")) for d in f.readlines()]:
            depths.append(depth)
    for i, depth in enumerate(depths):
        try:
            if depths[i+3] > depth:
                increases += 1
        except IndexError:
            break
    print(increases)

if __name__ in "__main__":
    part1()
    part2()