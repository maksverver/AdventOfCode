import sys

DIRS = (
    (-1, -1), (-1,  0), (-1,  1),
    ( 0, -1),           ( 0,  1),
    ( 1, -1), ( 1,  0), ( 1,  1),
)

grid = [line.strip() for line in sys.stdin]
H = len(grid)
W = len(grid[0])

def Letter(r, c):
    return grid[r][c] if 0 <= r < H and 0 <= c < W else '#'

def Part1():
    return sum(
        all(Letter(r + i*dr, c + i*dc) == ch for i, ch in enumerate('XMAS'))
        for r in range(H) for c in range(W) for dr, dc in DIRS)

def Part2():
    return sum(
        grid[r - 1][c - 1] + grid[r + 1][c + 1] in ('MS', 'SM') and
        grid[r - 1][c + 1] + grid[r + 1][c - 1] in ('MS', 'SM')
        for r in range(1, H - 1) for c in range(1, W - 1) if grid[r][c] == 'A')

print(Part1())
print(Part2())
