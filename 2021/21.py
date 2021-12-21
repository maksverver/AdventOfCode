from memoize import Memoize
import sys

def Part1(p, q):
    rolls = 0

    def Roll():
        nonlocal rolls
        d = rolls % 100 + 1
        rolls += 1
        return d

    pos = [p - 1, q - 1]
    score = [0, 0]
    p = 0
    while score[1 - p] < 1000:
        pos[p] += Roll() + Roll() + Roll()
        pos[p] %= 10
        score[p] += pos[p] + 1
        p = 1 - p
    return rolls * score[p]

def CalculateDiracRolls():
    '''Returns a list (r, n) where n is the number of ways to roll a total of r (mod 10).'''
    rolls = [0]*10
    for x in range(3):
        for y in range(3):
            for z in range(3):
                rolls[(x + y + z + 3)%10] += 1
    return [(r, n) for r, n in enumerate(rolls) if n > 0]

def Part2(p, q):
    rolls = CalculateDiracRolls()

    @Memoize
    def Calc(pos1, pos2, score1, score2):
        wins1 = wins2 = 0
        for r, n in rolls:
            new_pos = (pos1 + r) % 10
            new_score = score1 + new_pos + 1
            if new_score >= 21:
                wins1 += n
                continue
            w2, w1 = Calc(pos2, new_pos, score2, new_score)
            wins1 += w1 * n
            wins2 += w2 * n
        return (wins1, wins2)

    wins = Calc(p - 1, q - 1, 0, 0)
    return max(wins)


line1 = sys.stdin.readline()
line2 = sys.stdin.readline()
assert line1.startswith('Player 1 starting position:')
assert line2.startswith('Player 2 starting position:')
p = int(line1.split(':')[1])
q = int(line2.split(':')[1])
assert 1 <= p <= 10
assert 1 <= q <= 10

print(Part1(p, q))
print(Part2(p, q))
