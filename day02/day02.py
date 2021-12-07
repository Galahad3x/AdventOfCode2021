
def part1():
    depth = 0
    displacement = 0
    with open("day02/input.txt", "r") as f:
        for direction, value in [l.rstrip(" ").split(" ") for l in f.readlines()]:
            if direction == "up":
                depth -= int(value)
            elif direction == "down":
                depth += int(value)
            elif direction == "forward":
                displacement += int(value)
    print(depth, displacement, depth*displacement)

def part2():
    depth = 0
    displacement = 0
    aim = 0
    with open("day02/input.txt", "r") as f:
        for direction, value in [l.rstrip(" ").split(" ") for l in f.readlines()]:
            if direction == "up":
                aim -= int(value)
            elif direction == "down":
                aim += int(value)
            elif direction == "forward":
                displacement += int(value)
                depth += aim * int(value)
    print(depth, displacement, depth*displacement)

if __name__ in "__main__":
    part1()
    part2()