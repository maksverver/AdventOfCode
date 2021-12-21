import sys

# Transitions line: 512 bits
transitions = sys.stdin.readline().rstrip()
assert len(transitions) == 1 << 9

# Empty seperator
line = sys.stdin.readline().strip()
assert not line

# Initial grid.
grid = [[ch == '#' for ch in line.rstrip()] for line in sys.stdin]

def Pad(grid, n):
    W = len(grid[0])
    return (
        [[False] * (n + W + n) for _ in range(n)] +
        [[False] * n + row + [False] * n for row in grid] +
        [[False] * (n + W + n) for _ in range(n)])

def Neighbors(r, c):
    return [(rr, cc) for rr in (r - 1, r, r + 1) for cc in (c - 1, c, c + 1)]

def Step(grid, default_bit):
    def Index(r, c):
        i = 0
        for rr, cc in Neighbors(r, c):
            bit = grid[rr][cc] if 0 <= rr < len(grid) and 0 <= cc < len(grid[rr]) else default_bit
            i += i + bit
        return i

    return [[transitions[Index(r, c)] == '#' for c in range(len(grid[r]))] for r in range(len(grid))]

def PopCount(grid):
    return sum(bit for row in grid for bit in row)


b0 = transitions[0] == '#'
s511 = transitions[511] == '#'
assert not (b0 and s511)

grid = Pad(grid, 50)
for step in range(50):
    if step == 2:
        print(PopCount(grid))
    grid = Step(grid, b0 and step % 2)
print(PopCount(grid))
