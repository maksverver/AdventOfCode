#!/usr/bin/env pypy3

from lib15 import *
from random import randint
import sys

max_x = max_y = 4_000_000
validate = True

# Large 1
#num_sensors = 200
#num_beacons = 10

# Large 2
#num_sensors = 5000
#num_beacons = 20

# Large 3
num_sensors = 20000
num_beacons = 100

# Large 4
# This doesn't really work
#num_sensors = 100000
#num_beacons = 500
#validate = False

goal_x = randint(0, max_x)
goal_y = randint(0, max_y)
#goal_y = max_y  # to generate a point on the boundary

# T
goal_x -= (goal_x + goal_y) % 2

sensors = []
beacons = []

for _ in range(num_sensors):
  # maybe sensors can also exist outside the grid?
  x = randint(-max_x//4, max_x + max_x//4)
  y = randint(-max_y//4, max_y + max_y//4)
  #x = randint(0, max_x)
  #y = randint(0, max_y)
  sensors.append((x, y))

for _ in range(num_beacons):
  # maybe beacons can also exist outside the grid?
  x = randint(-max_x//4, max_x + max_x//4)
  y = randint(-max_y//4, max_y + max_y//4)
  #x = randint(0, max_x)
  #y = randint(0, max_y)
  # See explanation for goal_x above
  x -= 1 - (x + y) % 2
  beacons.append((x, y))

coords = []

for x, y in sensors:
  nearest_beacon = None
  beacon_dist = None
  for bx, by in beacons:
    d = abs(x - bx) + abs(y - by)
    if d == beacon_dist:
      print(x, y, '/', bx, by, '/', *nearest_beacon, file=sys.stderr)
    assert d != beacon_dist  # no ties allowed!
    if nearest_beacon is None or d < beacon_dist:
      beacon_dist = d
      nearest_beacon = bx, by
  bx, by = nearest_beacon

  goal_dist = abs(x - goal_x) + abs(y - goal_y)
  assert goal_dist != beacon_dist
  if goal_dist < beacon_dist:
    dx = goal_x - bx
    dy = goal_y - by
    assert((dx % 2 == 0) != (dy % 2 == 0))
    # Lame: just put it in the middle (rounding towards beacon)
    if dx % 2 == 1:
      dx += -1 if dx > 0 else +1
    if dy % 2 == 1:
      dy += -1 if dy > 0 else +1
    assert dx % 2 == 0 and dy % 2 == 0
    x = bx + dx // 2
    y = by + dy // 2
    beacon_dist = abs(x - bx) + abs(y - by)
    goal_dist = abs(x - goal_x) + abs(y - goal_y)
    assert beacon_dist == goal_dist - 1

    # Re-check that there are no ties for the nearest beacon
    for nbx, nby in beacons:
      d = abs(x - nbx) + abs(y - nby)
      assert d >= beacon_dist
      if d == beacon_dist:
        assert (bx, by) == (nbx, nby)

  print('Sensor at x={}, y={}: closest beacon is at x={}, y={}'.format(x, y, bx, by))
  coords.append((x, y, bx, by))

# Validate solution and check uniqueness
solutions = None
if validate:
  from solve import GeneratePart2Candidates
  solutions = list(GeneratePart2Candidates(MakeSensors(coords), max_x, max_y))

answer = 4000000 * goal_x + goal_y
print('solutions={} goal={} answer={}'.format(len(solutions) if validate else 'n/a', (goal_x, goal_y), answer), file=sys.stderr)

#from visualize import DrawImage
#DrawImage(coords, max_x=max_x, max_y=max_y, scale=1000).show()

if validate:
  assert(len(solutions) == 1)
  assert (goal_x, goal_y) in solutions
