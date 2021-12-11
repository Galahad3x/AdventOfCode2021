opening_items = ["[","{","(","<"]
closing_items = ["]","}",")",">"]

scores1 = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

scores2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def part1():
    incorrect_closings = []
    with open("day10/input.txt","r") as f:
        for line in [ln.rstrip("\n") for ln in f.readlines()]:
            stack = []
            for c in line:
                if c in opening_items:
                    stack.append(closing_items[opening_items.index(c)])
                elif c in closing_items:
                    cl = stack.pop()
                    if c != cl:
                        incorrect_closings.append(c)
    print("Part 1: ", sum(map(lambda x: scores1[x],incorrect_closings)))

def part2():
    incorrect_closings = []
    auto_scores = []
    with open("day10/input.txt","r") as f:
        for line in [ln.rstrip("\n") for ln in f.readlines()]:
            stack = []
            incorrect = False
            for c in line:
                if c in opening_items:
                    stack.append(closing_items[opening_items.index(c)])
                elif c in closing_items:
                    cl = stack.pop()
                    if c != cl:
                        incorrect = True
            if not incorrect:
                print(line, " | ", "".join(stack))
                score = 0
                stack_len = len(stack)
                for i in range(stack_len):
                    score *= 5
                    score += scores2[stack.pop()]
                auto_scores.append(score)
    auto_scores.sort()
    print(auto_scores)
    print("Part 2: ", auto_scores[(len(auto_scores) // 2)])


if __name__ in "__main__":
    part1()
    part2()