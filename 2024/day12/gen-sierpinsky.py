# Gnerates a grid in the form of a Sierpinski carpet:
#
#    #########
#    #.##.##.#
#    #########
#    ###...###
#    #.#...#.#
#    ###...###
#    #########
#    #.##.##.#
#    #########
#

from random import randrange, shuffle
from math import *
import sys

size = int(sys.argv[1])
assert log(size, 3) == round(log(size, 3))

grid = [['A' for _ in range(size)] for r in range(size)]

def PokeHoles(r, c, size):
    if size == 1:
        return
    assert size > 0 and size % 3 == 0
    size //= 3
    r0, r1, r2, r3 = (r + i*size for i in range(4))
    c0, c1, c2, c3 = (c + i*size for i in range(4))
    ch = chr(ord('a') + randrange(1, 26))
    for r in range(r1, r2):
        for c in range(c1, c2):
            grid[r][c] = ch
    PokeHoles(r0, c0, size)
    PokeHoles(r0, c1, size)
    PokeHoles(r0, c2, size)
    PokeHoles(r1, c0, size)
    PokeHoles(r1, c2, size)
    PokeHoles(r2, c0, size)
    PokeHoles(r2, c1, size)
    PokeHoles(r2, c2, size)

PokeHoles(0, 0, size)

for row in grid:
    print(''.join(row))
