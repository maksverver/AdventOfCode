# Advent of Code 2025 day 9 (https://adventofcode.com/2025/day/9)
#
# This solution draws the figure in a grid with compressed coordinates.
# The grid is then used to determine whether a particular rectangle completely
# overlaps the figure.

from itertools import combinations
import sys

coords = [tuple(map(int, line.split(','))) for line in sys.stdin]

# Part 1: maximum area of any rectangle
print(max((abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for ((x1, y1), (x2, y2)) in combinations(coords, 2)))

# For part 2, we will compress the coordinates
xs = sorted(set(x for x, _ in coords for x in (x - 1, x, x + 1)))
ys = sorted(set(y for _, y in coords for y in (y - 1, y, y + 1)))

xs_index = dict((x, i) for i, x in enumerate(xs))
ys_index = dict((y, i) for i, y in enumerate(ys))

# Create an empty grid (all cells marked '?')
W = len(xs)
H = len(ys)
grid = [['?']*W for _ in range(H)]

# Draw the outline of the figure with '#' characters.
for (x1, y1), (x2, y2) in zip(coords, coords[1:] + coords[:1]):
    cx1, cy1 = xs_index[x1], ys_index[y1]
    cx2, cy2 = xs_index[x2], ys_index[y2]
    assert (cx1 == cx2) != (cy1 == cy2)  # each segment is horizontal/vertical
    for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
        for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
            grid[y][x] = '#'

# Label cells outside the drawn figure as '.', using flood fill.
grid[0][0] = '.'
todo = [(0, 0)]
for x1, y1 in todo:
    for x2, y2 in ((x1 - 1, y1), (x1, y1 - 1), (x1 + 1, y1), (x1, y1 + 1)):
        if 0 <= x2 < W and 0 <= y2 < H and grid[y2][x2] == '?':
            grid[y2][x2] = '.'
            todo.append((x2, y2))

# Label remaining cells inside ('#')
grid = [''.join(row).replace('?', '#') for row in grid]

#for row in grid: print(row)  # Debug print the final grid

def Covered(x1, y1, x2, y2):
    '''Returns whether rectangle (x1,y1)-(x2,y2) of the grid contains only '#'.'''
    cx1, cy1 = xs_index[x1], ys_index[y1]
    cx2, cy2 = xs_index[x2], ys_index[y2]
    return all(grid[y][x] == '#'
            for x in range(min(cx1, cx2), max(cx1, cx2) + 1)
            for y in range(min(cy1, cy2), max(cy1, cy2) + 1))

# Part 2: find the maximum area across all possible rectangles that cover the figure.
# Same as the solution for part 1, except for the call to Covered().
print(max((abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for ((x1, y1), (x2, y2)) in combinations(coords, 2)
        if Covered(x1, y1, x2, y2)))
