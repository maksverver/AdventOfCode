# Generates a bunch of random pieces across a larger field.
#
# Suggested sizes: 5000. Mostly punishes solutions that don't drop pieces
# efficiently.

import sys
from random import *

N, = map(int, sys.argv[1:])

beams = []

z = 1
for i in range(N):
  z += randint(0, 5)
  x1 = x2 = randint(51, 100)
  y1 = y2 = randint(51, 100)
  z1 = z2 = z
  kind = randrange(0, 3)
  if kind == 0: x2 += randint(-50, 50)
  if kind == 1: y2 += randint(-50, 50)
  if kind == 2:
    z2 += randint(0, 9)
    if randint(0, 1): z1, z2 = z2, z1
  beams.append((x1, y1, z1, x2, y2, z2))
  z = z2 + 1

shuffle(beams)
for beam in beams:
  print('%d,%d,%d~%d,%d,%d' % beam)
