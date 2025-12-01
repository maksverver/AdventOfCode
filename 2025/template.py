from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heappush, heappop
from math import * # pyright: ignore[reportWildcardImportFromLibrary]
from operator import mul
import re
import sys

# Read ints
#a = [int(s) for s in sys.stdin]

# Read rows of ints
#a = [[int(s) for s in line.split()] for line in sys.stdin]

# Read a grid of characters.
#grid = [list(line.strip()) for line in sys.stdin]
#H = len(grid)
#W = len(grid[0])
# see also grid-2d.py for other useful functions

# Alternatively, grid as a dictionary (this is often easier to work with!)
#grid = {(r, c): ch
#        for r, line in enumerate(sys.stdin)
#        for c, ch in enumerate(line.strip())}

# Read parts separated by double newlines.
#part1, part2 = sys.stdin.read().strip().split('\n\n')
#lines1 = part1.split('\n')
#lines2 = part2.split('\n')

# Parsing regular expressions (see ../library-code/regex.py for more)
#PATTERN = re.compile(r'^foo (\d*) bar (\d*) baz$')
#for line in sys.stdin:
#  a, b = PATTERN.match(line).groups()
#  a, b = map(int, PATTERN.match(line).groups())
#  print(a + b)

answer = 0
print(answer)
