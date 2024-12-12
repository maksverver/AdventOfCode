import sys

grid = [line.strip() for line in sys.stdin]
H = len(grid)
W = len(grid[0])
assert all(len(row) == W for row in grid)

# maps vertex to region id
index = [[-1]*W for _ in range(H)]

def FloodFill(i, r, c):
    index[r][c] = i
    region = [(r, c)]
    perimeter = 0
    for (r, c) in region:
        for (r2, c2) in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
            if 0 <= r2 < H and 0 <= c2 < W and grid[r2][c2] == grid[r][c]:
                if index[r2][c2] == -1:
                    index[r2][c2] = i
                    region.append((r2, c2))
            else:
                perimeter += 1
    return len(region), perimeter

regions = 0
areas = []

# Part 1
#
# Flood fill all regions to find their areas and the length of their perimeters.
answer1 = 0
for r in range(H):
    for c in range(W):
        if index[r][c] == -1:
            # Part 1: flood fill to find area and perimeter
            area, perimeter = FloodFill(regions, r, c)
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
        i = index[r    ][c    ] if 0 <= r     < H and 0 <= c     < W else -1
        j = index[r    ][c + 1] if 0 <= r     < H and 0 <= c + 1 < W else -1
        k = index[r + 1][c    ] if 0 <= r + 1 < H and 0 <= c     < W else -1
        l = index[r + 1][c + 1] if 0 <= r + 1 < H and 0 <= c + 1 < W else -1
        for _ in range(4):
            if i >= 0 and ((j == k == i != l) or (j != i != k)):
                corners[i] += 1
            i, j, l, k = j, l, k, i  # rotate 90 degrees
print(sum(a * c for a, c in zip(areas, corners)))
