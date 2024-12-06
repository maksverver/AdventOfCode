import sys

# Directions in clockwise order: up, right, down, left
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

grid = [list(line.strip()) for line in sys.stdin]
H = len(grid)
W = len(grid[0])

start, = [(r, c) for r in range(H) for c in range(W) if grid[r][c] == '^']

# Plots out the path taken by the guard, and returns a pair:
#
#   - boolean indicating whether the guard exited (False) or the path loops (True)
#   - set of visited states (r, c, dir)
#
def FindPath(blocked=None):
    (r, c), dir = start, 0
    states = set()
    while (r, c, dir) not in states:
        states.add((r, c, dir))
        dr, dc = DIRS[dir]
        r2, c2 = r + dr, c + dc
        if not (0 <= r2 < H and 0 <= c2 < W):
            return False, states  # guard exited
        if grid[r2][c2] == '#' or (r2, c2) == blocked:
            dir = (dir + 1) % 4
        else:
            r, c = r2, c2
    return True, states  # loop detected

# Part 1: find the number of different positions in the path of the guard.
loops, states = FindPath()
assert not loops
positions = set((r, c) for (r, c, dir) in states)
print(len(positions))

# Part 2: find the number of positions we could block to cause a loop.
print(sum(FindPath(pos)[0] for pos in positions if pos != start))
