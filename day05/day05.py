def read_input(filter1=True):
	lines = []
	with open("input.txt", "r") as f:
		for line in [ln.rstrip("\n") for ln in f.readlines()]:
			start, end = line.split(" -> ")
			x1, y1 = start.split(",")
			x2, y2 = end.split(",")
			if filter1:
				if x1 == x2 or y1 == y2:
					lines.append(((int(x1), int(y1)), (int(x2), int(y2))))
			else:
				lines.append(((int(x1), int(y1)), (int(x2), int(y2))))
	return lines


def part1(lines_info):
	width = max([l[0][0] for l in lines_info] + [l[1][0] for l in lines_info]) + 1
	height = max([l[0][1] for l in lines_info] + [l[1][1] for l in lines_info]) + 1
	lines_map = []
	for i in range(height):
		lines_map.append([0] * width)
	for line in lines_info:
		print(line)
		start, end = line
		x1, y1 = start
		x2, y2 = end
		if x1 == x2:
			h_dir = 0
		elif x1 > x2:
			h_dir = -1
		else:
			h_dir = 1
		if y1 == y2:
			v_dir = 0
		elif y1 > y2:
			v_dir = -1
		else:
			v_dir = 1
		sx = x1
		sy = y1
		lines_map[sy][sx] += 1
		while sx != x2 or sy != y2:
			sx += h_dir
			sy += v_dir
			lines_map[sy][sx] += 1
	counter = 0
	for ln in lines_map:
		print(ln)
		for elem in ln:
			if elem >= 2:
				counter += 1
	print(counter)


if __name__ in "__main__":
	lines_info = read_input(False)
	part1(lines_info)
