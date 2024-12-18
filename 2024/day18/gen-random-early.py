# Random case that fails at `size`
#
# (This means the minimum size must be 1025)

from random import shuffle
import sys

size = 2501

antidiagonal = [(r, c) for r in range(size) for c in range(size) if r == size - 1 - c]
others = [(r, c) for r in range(size) for c in range(size) if r != size - 1 - c and (r, c) != (0, 0) and (r, c) != (size-1,size-1)]
shuffle(antidiagonal)
shuffle(others)
for r, c in antidiagonal + others:
    print(c, r, sep=',')
print('t', len(antidiagonal) - 1, sep='=', file=sys.stderr)
r, c = antidiagonal[-1]
print(c, r, sep=',', file=sys.stderr)
