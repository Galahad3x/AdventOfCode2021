import numpy as np

def part1():
    report = []
    with open("day03/input.txt") as f:
        for elem in [ln.rstrip("\n") for ln in f.readlines()]:
            report.append(np.array([e for e in elem]))
    repor = np.array(report)
    gammarate = ""
    epsilonrate = ""
    for col in repor.T:
        print(col)
        zeros = 0
        ones = 0
        for elem in col:
            if elem == "0":
                zeros += 1
            else:
                ones += 1
        if zeros > ones:
            gammarate += "0"
            epsilonrate += "1"
        else:
            gammarate += "1"
            epsilonrate += "0"
    print(gammarate, epsilonrate)
    print(int(gammarate, base=2) * int(epsilonrate, base=2))

def part2():
    report = []
    with open("day03/input.txt") as f:
        for elem in [ln.rstrip("\n") for ln in f.readlines()]:
            report.append(np.array([e for e in elem]))
    repor = np.array(report)
    oxygen_ratio = np.copy(repor)
    oxy_ratio = np.copy(oxygen_ratio)
    co2_ratio = np.copy(repor)
    co_ratio = np.copy(co2_ratio)
    for i, col in enumerate(oxygen_ratio.T):
        zeros = 0
        ones = 0
        for elem in oxy_ratio[:,i]:
            if elem == "0":
                zeros += 1
            else:
                ones += 1
        if zeros == ones:
            oxy2_ratio = []
            for elem in oxygen_ratio:
                if "".join(elem) in ["".join(e) for e in oxy_ratio] and elem[i] == "1":
                    oxy2_ratio.append(elem)
            oxy_ratio = np.array(oxy2_ratio)
        elif zeros > ones:
            oxy2_ratio = []
            for elem in oxygen_ratio:
                if "".join(elem) in ["".join(e) for e in oxy_ratio] and elem[i] == "0":
                    oxy2_ratio.append(elem)
            oxy_ratio = np.array(oxy2_ratio)
        else:
            oxy2_ratio = []
            for elem in oxygen_ratio:
                if "".join(elem) in ["".join(e) for e in oxy_ratio] and elem[i] == "1":
                    oxy2_ratio.append(elem)
            oxy_ratio = np.array(oxy2_ratio)
        if len(oxy_ratio) == 1:
            break
    for i, col in enumerate(co2_ratio.T):
        zeros = 0
        ones = 0
        for elem in co_ratio[:,i]:
            if elem == "0":
                zeros += 1
            else:
                ones += 1
        if zeros == ones:
            coo2_ratio = []
            for elem in co2_ratio:
                if "".join(elem) in ["".join(e) for e in co_ratio] and elem[i] == "0":
                    coo2_ratio.append(elem)
            co_ratio = np.array(coo2_ratio)
        elif zeros > ones:
            coo2_ratio = []
            for elem in co2_ratio:
                if "".join(elem) in ["".join(e) for e in co_ratio] and elem[i] == "1":
                    coo2_ratio.append(elem)
            co_ratio = np.array(coo2_ratio)
        else:
            coo2_ratio = []
            for elem in co2_ratio:
                if "".join(elem) in ["".join(e) for e in co_ratio] and elem[i] == "0":
                    coo2_ratio.append(elem)
            co_ratio = np.array(coo2_ratio)
        if len(co_ratio) == 1:
            break
    print("".join(oxy_ratio[0]))
    print("".join(co_ratio[0]))
    print(int("".join(oxy_ratio[0]), base=2)*int("".join(co_ratio[0]), base=2))

            


if __name__ in "__main__":
    part2()