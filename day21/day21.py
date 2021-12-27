import itertools

def part1():
    ddice = 0
    rolls = 0
    player1 = 4
    player2 = 9
    player1_s = 0
    player2_s = 0
    # True is player 1
    turn = True
    while player1_s < 1000 and player2_s < 1000:
        if turn:
            player1_t = 0
            for _ in range(3):
                player1_t += (ddice + 1)
                ddice = ((ddice + 1) % 100)
                rolls += 1
            player1 = ((player1 + player1_t) % 10)
            if player1 == 0:
                player1 = 10
            player1_s += player1
            if player1_s >= 1000:
                    break
            turn = not turn
        else:
            player2_t = 0
            for _ in range(3):
                player2_t += (ddice + 1)
                ddice = ((ddice + 1) % 100)
                rolls += 1
            player2 = ((player2 + player2_t) % 10)
            if player2 == 0:
                player2 = 10
            player2_s += player2
            if player2_s >= 1000:
                    break
            turn = not turn
    print("Part 1:", player1_s, player2_s, min(player1_s,player2_s) * rolls)

def who_wins(player1, player1_s, player2, player2_s, turn):
    if player1_s >= 21:
        return 1, 0
    if player2_s >= 21:
        return 0, 1
    player1_w, player2_w = 0, 0
    if turn:
        turns_done = {}
        for trn in itertools.product([1,2,3], repeat=3):
            player1_t = sum(trn)
            if player1_t in turns_done:
                player1_w += turns_done[player1_t][0]
                player2_w += turns_done[player1_t][1]
            else:
                player11 = (player1 + player1_t) % 10
                if player11 == 0:
                    player11 = 10
                wins1, wins2 = who_wins(player11, player1_s + player11, player2, player2_s, False)
                player1_w += wins1
                player2_w += wins2
                turns_done[player1_t] = [wins1, wins2]
    else:
        turns_done = {}
        for trn in itertools.product([1,2,3], repeat=3):
            player2_t = sum(trn)
            if player2_t in turns_done:
                player1_w += turns_done[player2_t][0]
                player2_w += turns_done[player2_t][1]
            else:
                player11 = (player2 + player2_t) % 10
                if player11 == 0:
                    player11 = 10
                wins1, wins2 = who_wins(player1, player1_s, player11, player2_s + player11, True)
                player1_w += wins1
                player2_w += wins2
                turns_done[player2_t] = [wins1, wins2]
    return player1_w, player2_w

    

def part2():
    print(who_wins(4, 0, 9, 0, True))

if __name__ in "__main__":
    part1()
    part2()