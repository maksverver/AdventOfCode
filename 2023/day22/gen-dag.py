# Generates bricks according to the pattern (in a single plane):
#
#
#           +-----+--+
#           |  e  | f|
#           +-----+--|
#           |  c  | d|
#        +--+--+--+--+
#        |  a  |  b  |
#        +-----+--+--+
#        +-----+--+
#        |     |  |
#        +-----+  |
#        |     |  |
#     +--+--+--+--+
#     |     |     |
#     +-----+--+--+
#     +-----+--+
#     |     |  |
#     +-----+  |
#     |     |  |
#  +--+--+--+--+
#  |     |     |
#  +-----+-----+
#  etc.
#
#
# (We could also do this in multiple dimensions but I'm too lazy to determine
# the equations.)
#
# If you define the parent of a block as the topmost block that can be removed
# to make it fall, then the blocks on the right all have nearby parents and
# therefore long chains of ancestors (f -> d -> b -> etc.), while the blocks on
# the left (e, c, a, etc.) have only the floor as their parent. This can be
# costly to figure out efficiently due to lack of a single bottleneck.
#
#  In DAG form this looks like:
#
#          e    f
#          |    |
#          c    d
#          |    |
#          a    b
#         /  \ /
#        o    o
#        |    |
#        o    o
#        |    |
#        o    o
#       /  \ /
#      o    o
#      |    |
#      o    |
#      |    |
#      o    o
#     /  \ /
#    o   o      floor
#   ------------------
#
#
# Suggested size: 200,000 to defeat quadratic-time solutions

import sys
from random import *

N, = map(int, sys.argv[1:])

beams = []

for i in range(N):
  x = i + 1
  y = 42
  #z1, z2, z3 = 3*i + 1, 3*i + 2, 3*i + 3     # compact z's
  z1, z2, z3 = 10*i + 1, 10*i + 4, 10*i + 7  # sparse z's

  beams.append(((x + 1, y, z1, x + 2, y, z1)))  # a
  beams.append(((x + 3, y, z1, x + 4, y, z1)))  # b
  beams.append(((x + 2, y, z2, x + 3, y, z2)))  # c
  beams.append(((x + 4, y, z2, x + 4, y, z2)))  # d
  beams.append(((x + 2, y, z3, x + 3, y, z3)))  # e
  beams.append(((x + 4, y, z3, x + 4, y, z3)))  # d

shuffle(beams)
for beam in beams:
  print('%d,%d,%d~%d,%d,%d' % beam)
