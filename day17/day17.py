target_x1 = 244
target_x2 = 303
target_y1 = -91
target_y2 = -54

def in_target_area(x, y):
    if x >= min(target_x1, target_x2) and x <= max(target_x1, target_x2):
        if y >= min(target_y1, target_y2) and y <= max(target_y1, target_y2):
            return True
    return False

def passed_target_area(x, y):
    if x > max(target_x1, target_x2) or y < min(target_y1,target_y2):
        return True
    return False

def step(x, y, x_v, y_v, max_y):
    x += x_v
    y += y_v
    if x_v > 0:
        x_v -= 1
    elif x_v < 0:
        x_v += 1
    y_v -= 1
    return x, y, x_v, y_v, max(max_y, y)

def part1():
    max_y = 0
    max_traj = None
    x_calc = True
    coord_sum = 0
    for x_v in range(max(target_x1, target_x2)+2000):
        for y_v in range(min(target_y1, target_y2) - 2000, max(target_x1, target_x2) + 2000):
            x, y, max_y_local = 0, 0, 0
            x_v_2 = x_v
            y_v_2 = y_v
            while not passed_target_area(x, y):
                if in_target_area(x, y):
                    print(x, y, max_y_local)
                    coord_sum += 1
                    if max_y_local > max_y:
                        max_y = max_y_local
                        max_traj = x, y
                    break
                else:
                    x, y, x_v_2, y_v_2, max_y_local = step(x, y, x_v_2, y_v_2, max_y_local)
    print(max_y, max_traj)
    print(coord_sum)


if __name__ in "__main__":
    part1()