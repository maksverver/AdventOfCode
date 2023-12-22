# Generates alternating horizontal and vertical beams that all overlap in
# the area x=50..100, y=50..100.
#
# For naive implementations, this makes the initial drop hard to calculate, and
# also makes it hard to calculate the sum of dropped pieces.
#
# Suggested sizes: 50,000 (large than 50,000 might not fit in int32)

import sys
from random import *

N, = map(int, sys.argv[1:])

beams = []

for i in range(N):
  cx = randrange(100, 150)
  z = randrange(50*i, 50*(i + 1))
  if i % 2 == 0:
    # Horizontal beam
    y = randint(50, 100)
    x1 = randint(1, 50)
    x2 = randint(100, 150)
    beams.append((x1, y, z, x2, y, z))
  else:
    # Vertical beam
    x = randint(50, 100)
    y1 = randint(1, 50)
    y2 = randint(100, 150)
    beams.append((x, y1, z, x, y2, z))

shuffle(beams)
for beam in beams:
  print('%d,%d,%d~%d,%d,%d' % beam)
