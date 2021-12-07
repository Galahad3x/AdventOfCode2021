from tqdm import tqdm

def calculate_fuel_1(positions, fuel):
    return sum([abs(pos-fuel) for pos in positions])

def create_fuel(fuel):
    def calculate_single_fuel(position):
        suma = diff = abs(position - fuel)
        for i in range(diff):
            suma += i
        return suma
    return calculate_single_fuel

def calculate_fuel(positions, fuel):
    fuels = map(create_fuel(fuel), positions)
    return sum([fue for fue in fuels])

def part1():
    with open("day07/input.txt","r") as f:
        positions = [int(n) for n in f.readlines()[0].rstrip("\n").split(",")]
    min_fuel = None
    min_pos = None
    for i in tqdm(range(max(positions))):
        fuel = calculate_fuel(positions, i)
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
            min_pos = i
    print(min_fuel, min_pos)

if __name__ in "__main__":
    part1()