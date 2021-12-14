from collections import Counter
from tqdm import tqdm

template = "HBCHSNFFVOBNOFHFOBNO"

def part1():
    subs = []
    not_subs = {}
    not_sub_c = 0
    with open("day14/input.txt", "r") as f:
        for pair, element in [ln.rstrip('\n').split(" -> ") for ln in f.readlines()]:
            subs.append((pair[0], pair[1], element))
    polymer = template
    for _ in tqdm(range(10)):
        print(len(polymer))
        polymer2 = ""
        for i, elem in enumerate(polymer[:-1]):
            for sub in subs:
                if sub[0] == elem and sub[1] == polymer[i+1]:
                    polymer2 += elem
                    polymer2 += sub[2]
                    break
            else:
                not_subs[str(not_sub_c)] = sub[0] + sub[1]
                polymer2 += str(not_sub_c)
                not_sub_c + 1
        polymer2 += polymer[-1]
        polymer = polymer2
    res_polymer = ""
    for elem in polymer:
        if elem in not_subs.keys():
            res_polymer += not_subs[elem]
        else:
            res_polymer += elem
    part_1 = max(Counter(res_polymer).values()) - min(Counter(res_polymer).values())
    print("Part 1: ", part_1)

def to_pairs(templ):
    pairs = {}
    for i, elem in enumerate(templ[:-1]):
        pairs[elem + templ[i+1]] = pairs.get(elem + templ[i+1], 0) + 1
    return pairs

def part2():
    subs = []
    pairs = {}
    with open("day14/input.txt", "r") as f:
        for pair, element in [ln.rstrip('\n').split(" -> ") for ln in f.readlines()]:
            subs.append((pair[0], pair[1], element))
    pairs = to_pairs(template)
    letters = Counter(template)
    for _ in tqdm(range(40)):
        new_pairs = {}
        for pair in pairs.keys():
            for sub in subs:
                if sub[0] == pair[0] and sub[1] == pair[1]:
                    new_pairs[pair] = new_pairs.get(pair,0) - pairs[pair]
                    new_pairs[pair[0] + sub[2]] = new_pairs.get(pair[0] + sub[2],0) + pairs[pair]
                    new_pairs[sub[2] + pair[1]] = new_pairs.get(sub[2] + pair[1],0) + pairs[pair]
                    letters[sub[2]] = letters.get(sub[2],0) + pairs[pair]
                    break
        for new_p in new_pairs.keys():
            pairs[new_p] = pairs.get(new_p, 0) + new_pairs[new_p]
    part_2 = max(letters.values()) - min(letters.values())
    print("Part 2: ", part_2)

if __name__ in "__main__":
    part2()