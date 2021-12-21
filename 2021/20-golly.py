# Converts Day 20 to a Golly pattern with a rule suitable for QuickLife.
#
# Example run:
#
#   python3 20-golly.py <testdata/20.in >day-20.rle
#   bgolly day-20.rle
#
# Will print population counts at each generation. The rle file can also be
# loaded in the Golly GUI, of course.

import sys

# Transitions line: 512 bits
transitions = [ch == '#' for ch in sys.stdin.readline().rstrip()]
assert len(transitions) == (1 << 9) == 512

# Empty seperator
line = sys.stdin.readline().strip()
assert not line

# Initial grid.
grid = [[ch == '#' for ch in line.rstrip()] for line in sys.stdin]

# Calculate rule in QuickLife MAP format: http://golly.sourceforge.net/Help/Algorithms/QuickLife.html
base64_digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
rule = 'MAP'
for i in range(0, 512, 6):
    v = 0
    for j in range(i, i + 6):
        v += v + (transitions[j] if j < len(transitions) else 0)
    assert 0 <= v < 64
    rule += base64_digits[v]

# Print pattern
H = len(grid)
W = max(len(row) for row in grid)
print(f'x = {W}, y = {H}, rule = {rule}')
pattern = ''
for i, row in enumerate(grid):
    for bit in row:
        pattern += 'bo'[bit]
    pattern += '$!'[i + 1 == H]
print(pattern)
