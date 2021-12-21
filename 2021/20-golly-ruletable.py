# Converts Day 20 to a Golly rule suitable for the RuleLoader algorithm.
#
# This doesn't work. The rule loader algorithm doesn't seem to support the B0
# rule correctly. If it did work it would likely be slower than QuickLife
# anyway.

import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <input>')
    sys.exit(1)

name = sys.argv[1]

# Transitions line: 512 bits
with open(name + '.in', 'rt') as f:
    transitions = [ch == '#' for ch in f.readline().rstrip()]
    assert len(transitions) == (1 << 9) == 512

    # Empty seperator
    line = f.readline().strip()
    assert not line

    # Initial grid.
    grid = [[ch == '#' for ch in line.rstrip()] for line in f]

# Write rule
with open(name + '.rule', 'wt') as f:
    print(f'@RULE {name}', file=f)
    print('@TABLE', file=f)
    print('n_states:2', file=f)
    print('neighborhood:Moore', file=f)
    print('symmetries:none', file=f)
    # Moore neighborhood: C,N,NE,E,SE,S,SW,W,NW,C'
    indices = [3*(1 - dr) + (1 - dc) for dr, dc in [(0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]]
    for i in range(1 << 9):
        print(''.join('01'[(i >> j)&1] for j in indices) + '01'[transitions[i]], file=f)


# Write pattern
with open(name + '.rle', 'wt') as f:
    H = len(grid)
    W = max(len(row) for row in grid)
    print(f'x = {W}, y = {H}, rule = {name}', file=f)
    pattern = ''
    for i, row in enumerate(grid):
        for bit in row:
            pattern += 'bo'[bit]
        pattern += '$!'[i + 1 == H]
    print(pattern, file=f)
