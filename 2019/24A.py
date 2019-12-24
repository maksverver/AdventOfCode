import sys

grid = tuple(tuple('.#'.index(ch) for ch in line.rstrip()) for line in sys.stdin)

def Next(grid):
    def CountNeighbors(r, c):
        return sum(grid[rr][cc]
            for (rr, cc) in ((r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1))
            if 0 <= rr < len(grid) and 0 <= cc < len(grid[rr]))

    def Update(old, neighbor_count):
        return neighbor_count == 1 if old else neighbor_count in (1, 2)

    return tuple(tuple(Update(old, CountNeighbors(r, c)) for c, old in enumerate(row))
        for r, row in enumerate(grid))

seen = set()
while grid not in seen:
    seen.add(grid)
    grid = Next(grid)
#for line in grid:
#    print(''.join('.#'[bug] for bug in line))
print(sum((1 << i) for i, bug in enumerate(bug for row in grid for bug in row) if bug))
