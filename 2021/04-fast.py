from collections import defaultdict
import sys

def Main(size):
    numbers = [int(w) for w in sys.stdin.readline().split(',')]
    index = defaultdict(list)  # {v: [(i, r, c),..]} such that card i, row r, col c has value v
    cards = 0
    sum_left = []  # sum_left[i] = sum of numbers left on card i
    while sys.stdin.readline():
        card_sum = 0
        for r in range(size):
            row = [int(w) for w in sys.stdin.readline().split()]
            assert len(row) == size
            for c, value in enumerate(row):
                index[value].append((cards, r, c))
                card_sum += value
        sum_left.append(card_sum)
        cards += 1

    first_win = None
    last_win = None
    complete = [False]*cards
    row_left = [[size]*size for _ in range(cards)]  # row_left[i][r] = numbers left in card i, row r
    col_left = [[size]*size for _ in range(cards)]  # col_left[i][c] = numbers left in card i, col c
    for num in numbers:
        for (i, r, c) in index[num]:
            if not complete[i]:
                row_left[i][r] -= 1
                col_left[i][c] -= 1
                sum_left[i] -= num
                if row_left[i][r] == 0 or col_left[i][c] == 0:
                    complete[i] = True
                    last_win = num * sum_left[i]
                    if first_win is None:
                        first_win = last_win
    print(first_win)
    print(last_win)

Main(size = 5)
