from math import floor
from random import choice, randrange, shuffle
import sys

# Large grid: 499 299 500000
# Small grid:  99  40   1000

height, width, num_moves = map(int, sys.argv[1:])

# This generates a relatively dense grid, with about 1 box pushed per move on average
p_wall = 0.0005
p_box  = 0.85

num_walls = floor(p_wall * height * width)
num_boxes = floor(p_box * height * width)
num_empty = height * width - num_walls - num_boxes - 1

chars = ['#']*num_walls + ['O']*num_boxes + ['.']*num_empty + ['@']
assert len(chars) == height * width
shuffle(chars)

grid = [chars[width*r:width*(r + 1)] for r in range(height)]

moves = ''.join(choice('^v<>') for _ in range(num_moves))

print((len(grid[0]) + 2) * '#')
for row in grid:
    print('#' + ''.join(row) + '#')
print((len(grid[0]) + 2) * '#')

print()
for i in range(0, len(moves), 80):
    print(moves[i:i+80])
