import sys

# Transitions line: 512 bits
transitions = sys.stdin.readline().strip()
assert len(transitions) == 1 << 9

# Empty seperator
line = sys.stdin.readline().strip()
assert not line

# Initial grid.
grid = {}
for r, line in enumerate(sys.stdin):
    for c, ch in enumerate(line):
        grid[r, c] = ch == '#'

def Neighbors(r, c):
    return [(rr, cc) for rr in (r - 1, r, r + 1) for cc in (c - 1, c, c + 1)]

def Step(grid, default):
    def Calculate(r, c):
        i = 0
        for rr, cc in Neighbors(r, c):
            i += i + grid.get((rr, cc), default)
        return transitions[i] == '#'

    candidates = set(p for ((r, c), v) in grid.items() for p in Neighbors(r, c))
    return {(r, c): Calculate(r, c) for (r, c) in candidates}


b0 = transitions[0] == '#'
s511 = transitions[511] == '#'
assert not (b0 and s511)

for step in range(50):
    if step == 2:
        print(sum(grid.values()))
    grid = Step(grid, b0 and step % 2)
print(sum(grid.values()))
