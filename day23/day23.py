from queue import PriorityQueue
import heapq

final_state = {"A1": 'A', "A2": 'A', "B1": 'B', "B2": 'B', "C1": 'C', "C2": 'C', "D1": 'D', "D2": 'D'}
move_cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

visited = {}


def to_string(state: dict):
	retval = ""
	for key in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]:
		if state.get(key):
			retval += state.get(key)
		retval += ","
	return retval


def draw(state: dict):
	print("#" * 13)
	print("#" + "".join([state.get(k, ".") for k in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]) + "#")
	print("###" + state.get("A1", ".") + "#" + state.get("B1", ".") + "#" + state.get("C1", ".") + "#" + state.get("D1",
	                                                                                                               ".") + "###")
	print("###" + state.get("A2", ".") + "#" + state.get("B2", ".") + "#" + state.get("C2", ".") + "#" + state.get("D2",
	                                                                                                               ".") + "###")
	print("#" * 13)


def state_heuristic(state: dict):
	start = 8000
	for elem in ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]:
		if state.get(elem):
			if state.get(elem) in elem:
				start -= 1000
	return start


def new_neighbour(state: dict):
	neighbour = {}
	for key, value in state.items():
		neighbour[key] = value[:]
	return neighbour


def find_neighbours(state: dict):
	neighbours = []
	for slot, amphi in state.items():
		slot = str(slot)
		if not slot.isnumeric():
			# In a hole
			if amphi in slot:
				# Own hole
				if "2" in slot:
					# Bottom part of correct hole so do nothing
					continue
				else:
					if state[amphi + "2"] == amphi:
						# Top part but bottom is correct so do nothing
						continue
					else:
						# Get out of the hole and into hallway
						possible_hallways = [0, 1, 3, 5, 7, 9, 10]
						hallway_hole = {"A": 2, "B": 4, "C": 6, "D": 8}[amphi]
						for hallway in possible_hallways:
							if hallway in state.keys():
								# Objective is blocked
								continue
							to_add = True
							for middle in range(min(hallway, hallway_hole), max(hallway, hallway_hole)):
								if middle in state.keys():
									# Middle is blocked
									to_add = False
									break
							if to_add:
								new_state = new_neighbour(state)
								new_state[hallway] = amphi
								del new_state[slot]
								distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 1) * move_cost[
									amphi]
								neighbours.append((distance, new_state))
			else:
				# In a hole, not the own hole
				if "2" in slot:
					if slot[0] + "1" in state.keys():
						# Blocked by another piece
						continue
				# Get out of the hole and into hallway
				possible_hallways = [0, 1, 3, 5, 7, 9, 10]
				hallway_hole = {"A": 2, "B": 4, "C": 6, "D": 8}[slot[0]]
				for hallway in possible_hallways:
					if hallway in state.keys():
						# Objective is blocked
						continue
					to_add = True
					for middle in range(min(hallway, hallway_hole), max(hallway, hallway_hole)):
						if middle in state.keys():
							# Middle is blocked
							to_add = False
							break
					if to_add:
						new_state = new_neighbour(state)
						new_state[hallway] = amphi
						del new_state[slot]
						distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 1) * move_cost[amphi]
						neighbours.append((distance, new_state))
				# Go from hole to hole, don't if that blocks another amphi
				hallway = {"A": 2, "B": 4, "C": 6, "D": 8}[amphi]
				# Go to bottom of hole if possible (needs both empty)
				if amphi + "2" not in state.keys() and amphi + "1" not in state.keys():
					if hallway in state.keys():
						# Objective is blocked
						continue
					to_add = True
					for middle in range(min(hallway, hallway_hole), max(hallway, hallway_hole)):
						if middle in state.keys():
							# Middle is blocked
							to_add = False
							break
					if to_add:
						new_state = new_neighbour(state)
						new_state[amphi + "2"] = amphi
						del new_state[slot]
						# +1 or +2 to get out + hallway + +2 to go in the bottom
						if slot[1] == "1":
							# Slot is on top
							distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 1 + 2) * move_cost[
								amphi]
						else:
							distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 2 + 2) * move_cost[
								amphi]
						neighbours.append((distance, new_state))
				# Go to top of hole if possible (needs bottom to be correct)
				if state.get(amphi + "2") == amphi and amphi + "1" not in state.keys():
					if hallway in state.keys():
						# Objective is blocked
						continue
					to_add = True
					for middle in range(min(hallway, hallway_hole), max(hallway, hallway_hole)):
						if middle in state.keys():
							# Middle is blocked
							to_add = False
							break
					if to_add:
						new_state = new_neighbour(state)
						new_state[amphi + "1"] = amphi
						del new_state[slot]
						# +1 or +2 to get out + hallway + +2 to go in the top
						if slot[1] == "1":
							# Slot is on top
							distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 1 + 1) * move_cost[
								amphi]
						else:
							distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 2 + 1) * move_cost[
								amphi]
						neighbours.append((distance, new_state))
		else:
			# In the hallway
			hallway_hole = int(slot)
			hallway = {"A": 2, "B": 4, "C": 6, "D": 8}[amphi]
			# Go to bottom of hole if possible (needs both empty)
			if amphi + "2" not in state.keys() and amphi + "1" not in state.keys():
				if hallway in state.keys():
					# Objective is blocked
					continue
				to_add = True
				for middle in range(min(hallway, hallway_hole) + 1, max(hallway, hallway_hole)):
					if middle in state.keys():
						# Middle is blocked
						to_add = False
						break
				if to_add:
					new_state = new_neighbour(state)
					new_state[amphi + "2"] = amphi
					del new_state[int(slot)]
					# hallway + +2 to go in the bottom
					distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 2) * move_cost[amphi]
					neighbours.append((distance, new_state))
			# Go to top of hole if possible (needs bottom to be correct)
			if state.get(amphi + "2") == amphi and amphi + "1" not in state.keys():
				if hallway in state.keys():
					# Objective is blocked
					continue
				to_add = True
				for middle in range(min(hallway, hallway_hole) + 1, max(hallway, hallway_hole)):
					if middle in state.keys():
						# Middle is blocked
						to_add = False
						break
				if to_add:
					new_state = new_neighbour(state)
					new_state[amphi + "1"] = amphi
					del new_state[int(slot)]
					# hallway + +1 to go in the top
					distance = (max(hallway, hallway_hole) - min(hallway, hallway_hole) + 1) * move_cost[amphi]
					neighbours.append((distance, new_state))
	return neighbours


def part1():
	start_state = {"A1": 'B', "A2": 'D', "B1": 'B', "B2": 'A', "C1": 'C', "C2": 'A', "D1": 'D', "D2": 'C'}
	# start_state = {"A1": 'A', "A2": 'A', 0: 'B', 1: 'B', "C1": 'C', "C2": 'C', "D1": 'D', "D2": 'D'}
	queue = []
	heapq.heapify(queue)
	heapq.heappush(queue, (0, 0, "", start_state))
	fc = []
	while len(queue) != 0:
		heuristic, cost, _, state = heapq.heappop(queue)
		# draw(state)
		if state == final_state:
			fc.append(cost)
			print(cost)
		neighbours = find_neighbours(state)
		for cost_of_move, neighbour in neighbours:
			found_cost = cost + cost_of_move
			if to_string(neighbour) not in visited:
				visited[to_string(neighbour)] = found_cost
				heapq.heappush(queue, (state_heuristic(neighbour), found_cost, str(neighbour), neighbour))
			else:
				found_cost_2 = min(visited[to_string(neighbour)], found_cost)
				visited[to_string(neighbour)] = found_cost_2
				if found_cost_2 == found_cost:
					heapq.heappush(queue, (state_heuristic(neighbour), found_cost_2, str(neighbour), neighbour))
	print(fc)


# print("Part 1: ", visited[str(final_state)])


if __name__ in "__main__":
	part1()
