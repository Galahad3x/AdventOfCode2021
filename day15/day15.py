def part1(risk_matrix2):
    path_matrix = []
    for i, risk_line in enumerate(risk_matrix2):
        path_line = []
        for j, elem in enumerate(risk_line):
            if j == 0:
                if i == 0:
                    path_line.append(0)
                else:
                    path_line.append(path_matrix[i-1][j] + elem)
            else:
                if i == 0:
                    path_line.append(path_line[j-1] + elem)
                else:
                    min_origin = min(path_matrix[i-1][j], path_line[j-1])
                    path_line.append(min_origin + elem)
        path_matrix.append(path_line)
    print(path_matrix[-1][-1])

def part2(risk_m):
    new_final_risk = []
    for elem in risk_m:
        new_final_risk.append(elem[:])
    for _ in range(4):
        for line in new_final_risk[-len(risk_m):]:
            new_final_risk.append([(n % 9) + 1 for n in line])
    for l_c, line in enumerate(new_final_risk):
        original_len = len(line)
        for h in range(4):
            for i in range(original_len):
                new_final_risk[l_c].append((line[h*original_len + i] % 9) + 1)
    return new_final_risk

if __name__ in "__main__":
    risk_matrix = []
    with open("day15/easy.txt", "r") as f:
        for line in [ln.rstrip('\n') for ln in f.readlines()]:
            risk_line2 = [int(n) for n in line]
            risk_matrix.append(risk_line2)
    print(len(risk_matrix))
    for line in risk_matrix:
        # print(line)
        pass
    print("___________")
    risk = part2(risk_matrix)
    for line in risk:
        print(line)
    part1(risk)