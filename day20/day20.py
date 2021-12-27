from tqdm import tqdm

with open("day20/enhancement.txt", "r") as f:
    enhancement = ""
    for c in f.read():
        if c in "#.":
            enhancement += c

def expand(image, infinite_char):
    original_len = len(image[0])
    new_image = []
    new_row = []
    for _ in range(original_len + 4):
        new_row.append(infinite_char)
    new_image.append(new_row)
    new_image.append(new_row[:])
    for _ , line in enumerate(image):
        new_line = [infinite_char, infinite_char] + [c for c in line] + [infinite_char, infinite_char]
        new_image.append(new_line)
    new_image.append(new_row[:])
    new_image.append(new_row[:])
    new_image_2 = []
    for line in new_image:
        new_image_2.append(line[:])
    for i, line in enumerate(new_image):
        for j, c in enumerate(line):
            lookup_matrix = [infinite_char] * 9
            ind = 0
            for mod in [-1, 0, 1]:
                for mod2 in [-1, 0, 1]:
                    try:
                        lookup_matrix[ind] = new_image[i + mod][j + mod2]
                    except IndexError:
                        pass
                    ind += 1
            lookup_in_bin = ["1" if c == "#" else "0" for c in lookup_matrix]
            index = int("".join(lookup_in_bin), base=2)
            new_image_2[i][j] = enhancement[index]
    return new_image_2


def part1():
    image = []
    infinite_char = "."
    with open("day20/input.txt", "r") as f:
        for line in [ln.rstrip('\n') for ln in f.readlines()]:
            image.append(line)
    image = expand(image, infinite_char)
    infinite_char = "#"
    image = expand(image, infinite_char)
    pixels = 0
    for line in image:
        for elem in line:
            if elem == "#":
                pixels += 1
    print("Part1: ", pixels)

def part2():
    image = []
    infinite_char = "."
    with open("day20/input.txt", "r") as f:
        for line in [ln.rstrip('\n') for ln in f.readlines()]:
            image.append(line)
    for i in tqdm(range(50)):
        image = expand(image, infinite_char)
        if infinite_char == ".":
            infinite_char = "#"
        else:
            infinite_char = "."
    pixels = 0
    for line in image:
        for elem in line:
            if elem == "#":
                pixels += 1
    print("Part2: ", pixels)


if __name__ in "__main__":
    part1()
    part2()