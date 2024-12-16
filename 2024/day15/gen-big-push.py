from random import randrange
import sys

height, = map(int, sys.argv[1:])
assert height % 2 == 1  # heigth must be odd
width = height // 2 + 2
rounds = height // 4  # ensures the move data is about half the size of the input

grid = [['.']*width for _ in range(height)]

for i in range(height):
    w = height//2 - abs(height//2 - i) - 1
    if w > 0:
        grid[i][1:w+1] = ['O']*w

grid[0][0] = '@'

moves = 'v'
for r in range(2, height - 2):
    d = abs(height//2 - r) + 1
    moves += 'v' + d*'>' + d*'<'
moves += '^' * (height - 3)

for _ in range(rounds):
    w1 = height//2 + randrange(0, 2)
    w2 = height//2 + randrange(0, 2)
    moves += ('>' * w1) + 'vv' + ('<' * w1) + ('v' * (height - 3))
    moves += ('>' * w2) + '^^' + ('<' * w2) + ('^' * (height - 3))


print((len(grid[0]) + 2) * '#')
for row in grid:
    print('#' + ''.join(row) + '#')
print((len(grid[0]) + 2) * '#')

print()
for i in range(0, len(moves), 80):
    print(moves[i:i+80])
