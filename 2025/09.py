# Advent of Code 2025 day 9 (https://adventofcode.com/2025/day/9)
#
# This solution draws the figure in a grid with compressed coordinates.
# The grid is then used to determine whether a particular rectangle completely
# overlaps the figure.

from itertools import combinations
import sys

points = [tuple(map(int, line.split(','))) for line in sys.stdin]

rectangles = []
for (x1, y1), (x2, y2) in combinations(points, 2):
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    rectangles.append(((x2 - x1 + 1)*(y2 - y1 + 1), x1, y1, x2 + 1, y2 + 1))
rectangles.sort(reverse=True)

# Part 1: maximum area of any rectangle
print(rectangles[0][0])

# For part 2, we will compress the coordinates
xs = sorted(set(x for x, _ in points for x in (x - 1, x, x + 1)))
ys = sorted(set(y for _, y in points for y in (y - 1, y, y + 1)))

xs_index = dict((x, i) for i, x in enumerate(xs))
ys_index = dict((y, i) for i, y in enumerate(ys))

# Create an empty grid (all cells marked '?')
W = len(xs)
H = len(ys)
grid = [['?']*W for _ in range(H)]

# Draw the outline of the figure with '#' characters.
for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
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

# Part 2: find the maximum area across all possible rectangles that cover the figure.
for area, x1, y1, x2, y2 in sorted(rectangles, key=lambda t: t[0], reverse=True):
    if all(grid[y][x] == '#'
            for x in range(xs_index[x1], xs_index[x2])
            for y in range(ys_index[y1], ys_index[y2])):
        print(area)
        break
