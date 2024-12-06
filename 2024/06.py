import sys

# Directions in clockwise order: up, right, down, left
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

grid = [list(line.strip()) for line in sys.stdin]
H = len(grid)
W = len(grid[0])

start, = [(r, c) for r in range(H) for c in range(W) if grid[r][c] == '^']

def FindPath(blocked=None):
    (r, c), dir = start, 0
    states = set()
    while (r, c, dir) not in states:
        states.add((r, c, dir))
        dr, dc = DIRS[dir]
        r2, c2 = r + dr, c + dc
        if not (0 <= r2 < H and 0 <= c2 < W):
            return states
        if grid[r2][c2] == '#' or (r2, c2) == blocked:
            dir = (dir + 1) % 4
        else:
            r, c = r2, c2
    return None

# Part 1
positions = set((r, c) for (r, c, dir) in FindPath())
print(len(positions))

# Part 2
print(sum(FindPath(pos) is None for pos in positions if pos != start))
