# Advent of Code 2024 day 12: Garden Groups
# https://adventofcode.com/2024/day/12
#
# Simpler implementation of part 2: count corners instead of tracing outlines.

import sys

grid = {(r, c): ch
        for r, line in enumerate(sys.stdin)
        for c, ch in enumerate(line.strip())}
H = max(r for r, c in grid)
W = max(c for r, c in grid)

# maps vertex to region id
index = {}

def FloodFill(i, start):
    index[start] = i
    region = [start]
    perimeter = 0
    for v in region:
        r, c = v
        for w in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
            if grid.get(w) != grid[v]:
                perimeter += 1
            elif w not in index:
                index[w] = i
                region.append(w)
    return len(region), perimeter

regions = 0
areas = []

# Part 1
#
# Flood fill all regions to find their areas and the length of their perimeters.
answer1 = 0
for v in grid:
    if v not in index:
        # Part 1: flood fill to find area and perimeter
        area, perimeter = FloodFill(regions, v)
        areas.append(area)
        regions += 1
        answer1 += area * perimeter
print(answer1)

# Part 2
#
# Detect all corners of regions. The number of straight segments on the perimeter
# is equal to the number of corners.
#
# Note that we can detect corners by scanning the grid and looking at each 2x2
# square of plots, where we count the center depending on whether the region
#
#   A z     Case 1: center point is a convex corner for region A.
#   x ?
#
#   A A     Case 2: center point is a concave corner for region A.
#   A x
#
# We must consider both these cases for all 4 corners; the code below simply rotates
# the 2x2 square 4 times to cover all cases.
#
# Special case to consider:
#
#   A x     in this case the center counts as two convex corners for different
#   y A     parts of region A, not a single corner.
#
# This is handled correctly automatically.
#
corners = [0]*regions
for r in range(-1, H + 1):
    for c in range(-1, W + 1):
        # i j
        # k l
        i = index.get((r    , c    ))
        j = index.get((r    , c + 1))
        k = index.get((r + 1, c    ))
        l = index.get((r + 1, c + 1))
        for _ in range(4):
            if (i is not None) and ((j == k == i != l) or (j != i != k)):
                corners[i] += 1
            i, j, l, k = j, l, k, i  # rotate 90 degrees
print(sum(a * c for a, c in zip(areas, corners)))
