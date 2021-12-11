from functools import reduce

def part1():
    grid = []
    with open("day09/input.txt","r") as f:
        for line in [ln.rstrip("\n") for ln in f.readlines()]:
            grid.append([int(n) for n in line])
    low_points = []
    for col_c, row in enumerate(grid):
        for row_c, elem in enumerate(row):
            print(col_c, row_c)
            e_add = True
            try:
                if row_c > 0:
                    if row[row_c-1] <= elem:
                        e_add = False
            except IndexError:
                pass
            try:
                if row[row_c+1] <= elem:
                    e_add = False
            except IndexError:
                pass
            try:
                if grid[col_c-1][row_c] <= elem:
                    e_add = False
            except IndexError:
                pass
            try:
                if grid[col_c+1][row_c] <= elem:
                    e_add = False
            except IndexError:
                pass
            if e_add:
                print(col_c, row_c, elem)
                low_points.append(elem)
    print(low_points)
    print("Part 1: ", sum([1+e for e in low_points]))

def get_basin(grid, col_c, row_c, added):
    elem = grid[col_c][row_c]
    if not added[col_c][row_c]:
        added[col_c][row_c] = True
    else:
        return []   
    basin = [elem]
    try:
        if row_c > 0:
            if grid[col_c][row_c-1] > elem:
                if grid[col_c][row_c-1] == 9:
                    # Basin wall
                    pass
                else:
                    basin.extend(get_basin(grid, col_c, row_c-1, added))
    except IndexError:
        pass
    try:
        if grid[col_c][row_c+1] > elem:
            if grid[col_c][row_c+1] == 9:
                # Basin wall
                pass
            else:
                basin.extend(get_basin(grid, col_c, row_c+1, added))
    except IndexError:
        pass
    try:
        if col_c > 0:
            if grid[col_c-1][row_c] > elem:
                if grid[col_c-1][row_c] == 9:
                    # Basin wall
                    pass
                else:
                    basin.extend(get_basin(grid, col_c-1, row_c, added))
    except IndexError:
        pass
    try:
        if grid[col_c+1][row_c] > elem:
                if grid[col_c+1][row_c] == 9:
                    # Basin wall
                    pass
                else:
                    basin.extend(get_basin(grid, col_c+1, row_c, added))
    except IndexError:
        pass
    return basin

def part2():
    grid = []
    with open("day09/input.txt","r") as f:
        for line in [ln.rstrip("\n") for ln in f.readlines()]:
            grid.append([int(n) for n in line])
    basins = []
    for col_c, row in enumerate(grid):
        for row_c, elem in enumerate(row):
            e_add = True
            try:
                if row_c > 0:
                    if row[row_c-1] <= elem:
                        e_add = False
            except IndexError:
                pass
            try:
                if row[row_c+1] <= elem:
                    e_add = False
            except IndexError:
                pass
            try:
                if grid[col_c-1][row_c] <= elem:
                    e_add = False
            except IndexError:
                pass
            try:
                if grid[col_c+1][row_c] <= elem:
                    e_add = False
            except IndexError:
                pass
            if e_add:
                taken = [[False for e in row] for row in grid]
                bas = get_basin(grid, col_c, row_c, taken)
                basins.append(bas)
    basins.sort(key=len, reverse=True)
    for basin in basins[:3]:
        print(len(basin), basin)
    print("Part 2: ", reduce(lambda x, y: x * y, [len(b) for b in basins[:3]]))

if __name__ in "__main__":
    part2()