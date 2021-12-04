import sys

class Card:
    def __init__(self, grid):
        self.grid = grid

    def Mark(self, value):
        for r in range(5):
            for c in range(5):
                if self.grid[r][c] == value:
                    self.grid[r][c] = None
                    return self.WonRow(r) or self.WonCol(c)
        return False

    def WonRow(self, r):
        return all(self.grid[r][c] is None for c in range(5))

    def WonCol(self, c):
        return all(self.grid[r][c] is None for r in range(5))

    def Sum(self):
        return sum(val for row in self.grid for val in row if val is not None)

# Read input.
numbers = [int(w) for w in sys.stdin.readline().split(',')]
grids = []
while sys.stdin.readline():
    grids.append([[int(w) for w in sys.stdin.readline().split()] for _ in range(5)])

# Solve!
first_win = None
last_win = None
cards = [Card(grid) for grid in grids]
for num in numbers:
    for card in list(cards):
        if card.Mark(num):
            cards.remove(card)
            last_win = num * card.Sum()
            if first_win is None:
                first_win = last_win
print(first_win)
print(last_win)
