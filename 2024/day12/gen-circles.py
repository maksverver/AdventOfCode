# Generates a test case with concentric circles

from random import randrange, shuffle
from math import *
import sys

size = int(sys.argv[1])

def CharAt(r, c):
    d = hypot(r - size/2, c - size/2) / 4
    return 'OX'[(d - floor(d)) < 0.5]

grid = [[CharAt(r, c) for c in range(size)] for r in range(size)]
for row in grid:
    print(''.join(row))
