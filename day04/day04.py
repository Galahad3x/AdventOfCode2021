import numpy as np

def read_input():
	with open("input.txt","r") as f:
		lines = f.readlines()
	calling_numbers = [int(n) for n in lines[0].split(",")]
	cards = []
	card = []
	for line in [ln.rstrip("\n") for ln in lines[1:]]:
		if line == "":
			if card != []:
				cards.append(card)
			card = []
		else:
			card_row = []
			for elem in line.split(" "):
				try:
					card_row.append(int(elem))
				except ValueError:
					pass
			card.append(np.array(card_row))
	if card != []:
		cards.append(np.array(card))
	return calling_numbers, np.array(cards)
	
def part1_winner(card, number):
	unmarked_sum = sum([sum([e if e != -1 else 0 for e in row]) for row in card])
	return unmarked_sum * number
	
def part1(calling_numbers, cards):
	for number in calling_numbers:
		for card in cards:
			for card_row in card:
				for i, num in enumerate(card_row):
					if num == number:
						card_row[i] = -1
		for card in cards:
			for card_row in card:
				for i, num in enumerate(card_row):
					if num != -1:
						break
				else:
					return part1_winner(card, number)
			for card_col in card.T:
				for i, num in enumerate(card_col):
					if num != -1:
						break
				else:
					return part1_winner(card, number)
			print(card)
			
def part2(calling_numbers, cards):
	winners = list(range(len(cards)))
	for number in calling_numbers:
		for card in cards:
			for card_row in card:
				for i, num in enumerate(card_row):
					if num == number:
						card_row[i] = -1
		for ci, card in enumerate(cards):
			for card_row in card:
				for i, num in enumerate(card_row):
					if num != -1:
						break
				else:
					if ci in winners:
						winners.remove(ci)
					if len(winners) == 0:
						return part1_winner(card, number)
			for card_col in card.T:
				for i, num in enumerate(card_col):
					if num != -1:
						break
				else:
					if ci in winners:
						winners.remove(ci)
					if len(winners) == 0:
						return part1_winner(card, number)
			print(card)
	

if __name__ in "__main__":
	calling_numbers, cards = read_input()
	print("Part 1: ", part1(calling_numbers, cards))
	print("Part 2: ", part2(calling_numbers, cards))
