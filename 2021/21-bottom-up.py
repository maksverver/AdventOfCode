def CalculateDiracRolls():
    '''Returns a list (r, n) where n is the number of ways to roll a total of r (mod 10).'''
    rolls = [0]*10
    for x in range(3):
        for y in range(3):
            for z in range(3):
                rolls[(x + y + z + 3)%10] += 1
    print(rolls)
    return [(r, n) for r, n in enumerate(rolls) if n > 0]

rolls = CalculateDiracRolls()

# wins[score1][score2][pos1][pos2] = (wins_for_player1, wins_for_player2)
wins = [[[[None for _ in range(10)] for _ in range(10)] for _ in range(21)] for _ in range(21)]

for score1, score2 in sorted(((x, y) for x in range(21) for y in range(21)), key=lambda scores: -sum(scores)):
    for pos1 in range(10):
        for pos2 in range(10):
            wins1 = wins2 = 0
            for r, n in rolls:
                new_pos = (pos1 + r) % 10
                new_score = score1 + new_pos + 1
                if new_score >= 21:
                    wins1 += n
                    continue
                w2, w1 = wins[score2][new_score][pos2][new_pos]
                wins1 += w1 * n
                wins2 += w2 * n
            wins[score1][score2][pos1][pos2] = (wins1, wins2)

assert wins[0][0][4 - 1][8 - 1] == (444356092776315, 341960390180808)  # sample data
assert wins[0][0][8 - 1][4 - 1] == (446968027750017, 271438145890854)  # official data
