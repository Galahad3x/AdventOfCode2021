import copy
import itertools
from math import floor, ceil

from tqdm import tqdm


class Node:
	def __init__(self, data, parent=None):
		self.left = None
		self.right = None
		self.data = data
		self.parent = parent
		self.level = 0

	def is_leaf(self):
		return self.left is None and self.right is None

	def to_string(self):
		if self.data is not None:
			return str(self.data)
		else:
			return "[" + self.left.to_string() + ", " + self.right.to_string() + "]"

	def explosion_possible(self):
		if not self.is_leaf():
			if self.left.level == 4 and not self.left.is_leaf():
				return True
			if self.right.level == 4 and not self.right.is_leaf():
				return True
			return self.left.explosion_possible() or self.right.explosion_possible()
		else:
			return None

	def find_next_explosion(self):
		if self.explosion_possible() is not None:
			if self.left.level == 4 and self.left.data is None:
				return self.left
			if self.right.level == 4 and self.right.data is None:
				return self.right
			if not self.is_leaf():
				next_left = self.left.find_next_explosion()
				if next_left is not None:
					return next_left
				else:
					return self.right.find_next_explosion()
			else:
				return None
		return None

	def find_left_leaf(self, explosion_node):
		if explosion_node.parent is None:
			return None
		if id(explosion_node) == id(explosion_node.parent.left):
			if explosion_node.parent is None:
				return None
			return self.find_left_leaf(explosion_node.parent)
		else:
			if explosion_node.parent.left.is_leaf():
				return explosion_node.parent.left
			else:
				return explosion_node.parent.left.find_rightmost_leaf()

	def find_rightmost_leaf(self):
		if self.is_leaf():
			return self
		else:
			return self.right.find_rightmost_leaf()

	def find_right_leaf(self, explosion_node):
		if explosion_node.parent is None:
			return None
		if id(explosion_node) == id(explosion_node.parent.right):
			if explosion_node.parent is None:
				return None
			return self.find_right_leaf(explosion_node.parent)
		else:
			if explosion_node.parent.right.is_leaf():
				return explosion_node.parent.right
			else:
				return explosion_node.parent.right.find_leftmost_leaf()

	def find_leftmost_leaf(self):
		if self.is_leaf():
			return self
		else:
			return self.left.find_leftmost_leaf()

	def print(self):
		if not self.is_leaf():
			self.left.print()
		print(self.data, self.level, self.is_leaf())
		if not self.is_leaf():
			self.right.print()

	def explode(self, explosion_node):
		left_leaf = self.find_left_leaf(explosion_node)
		right_leaf = self.find_right_leaf(explosion_node)
		new_node = Node(0, parent=explosion_node.parent)
		if id(explosion_node) == id(explosion_node.parent.left):
			explosion_node.parent.left = new_node
		else:
			explosion_node.parent.right = new_node
		new_node.level = explosion_node.level
		if left_leaf is not None:
			left_leaf.data += explosion_node.left.data
		if right_leaf is not None:
			right_leaf.data += explosion_node.right.data

	def find_next_split(self):
		if self.is_leaf() and self.data >= 10:
			return self
		elif self.is_leaf():
			return None
		else:
			left_split = self.left.find_next_split()
			if left_split is not None:
				return left_split
			else:
				return self.right.find_next_split()

	def split(self, split_node):
		split_node.left = Node(floor(split_node.data / 2), parent=split_node)
		split_node.left.level = split_node.level + 1
		split_node.right = Node(ceil(split_node.data / 2), parent=split_node)
		split_node.right.level = split_node.level + 1
		split_node.data = None

	def reduced(self):
		next_explosion = self.find_next_explosion()
		if next_explosion is not None:
			self.explode(next_explosion)
			return self.reduced()
		next_split = self.find_next_split()
		if next_split is not None:
			self.split(next_split)
			return self.reduced()
		return self

	def increase(self):
		self.level += 1
		if not self.is_leaf():
			self.left.increase()
			self.right.increase()

	def magnitude(self):
		if self.is_leaf():
			return self.data
		else:
			return 3 * self.left.magnitude() + 2 * self.right.magnitude()


def add(pair1, pair2):
	root = Node(None)
	root.left = pair1
	pair1.parent = root
	pair1.increase()
	root.right = pair2
	pair2.parent = root
	pair2.increase()
	return root.reduced()


def string_to_nodes(string):
	root = Node(None)
	latest_open = root
	latest_level = 0
	for i, c in enumerate(string):
		if c == "[":
			latest_level += 1
			latest_open.left = Node(None, parent=latest_open)
			latest_open.left.level = latest_level
			latest_open = latest_open.left
		elif c in "0123456789":
			latest_open.data = int(c)
		elif c == ",":
			latest_open.parent.right = Node(None, parent=latest_open.parent)
			latest_open.parent.right.level = latest_level
			latest_open = latest_open.parent.right
		else:
			latest_level -= 1
			latest_open = latest_open.parent
	return root


def part1():
	total_snail_sum = ""
	with open("input.txt", "r") as f:
		for i, line in enumerate([ln.rstrip("\n") for ln in f.readlines()]):
			if i == 0:
				total_snail_sum = string_to_nodes(line)
			else:
				tree_line = string_to_nodes(line)
				total_snail_sum = add(total_snail_sum, tree_line)
	print("Part 1:", total_snail_sum.magnitude())


def part2():
	trees = []
	max_magnitude = 0
	with open("input.txt", "r") as f:
		for i, line in enumerate([ln.rstrip("\n") for ln in f.readlines()]):
			trees.append(string_to_nodes(line))
	for tree in tqdm(trees):
		for tree2 in trees:
			magnitude = add(copy.deepcopy(tree), copy.deepcopy(tree2)).magnitude()
			if magnitude > max_magnitude:
				max_magnitude = magnitude
	print("Part 2:", max_magnitude)


if __name__ in "__main__":
	part1()
	part2()
