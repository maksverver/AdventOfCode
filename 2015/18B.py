import sys

def count_nearby(grid, r1, c1):
	res = 0
	for r2 in range(max(0, r1 - 1), min(r1 + 2, len(grid))):
		for c2 in range(max(0, c1 - 1), min(c1 + 2, len(grid[r2]))):
			res += grid[r2][c2]
	return res

def update(r, c, val, nearby):
	return nearby == 3 or (val and nearby == 4)

def step(grid):
	return [ [ update(i, j, val, count_nearby(grid, i, j))
	           for j,val in enumerate(row) ]
	         for i,row in enumerate(grid) ]

def fix(grid):
	grid[0][0] = grid[0][-1] = grid[-1][0] = grid[-1][-1] = True

grid = [ [ c == '#' for c in line.strip() ] for line in sys.stdin ]
fix(grid)
for _ in range(100):
	grid = step(grid)
	fix(grid)
print sum(sum(row) for row in grid)
