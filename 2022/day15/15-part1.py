from math import inf
import re
import sys

#target_y = 10
target_y = 2000000

beacon_xs = set()

ranges = []

for line in sys.stdin:
  m = re.match('^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$', line)
  sx, sy, bx, by = map(int, m.groups())
  range = abs(sx - bx) + abs(sy - by)
  dx = range - abs(sy - target_y)
  if dx >= 0:
    ranges.append((sx - dx, sx + dx))
  if by == target_y:
    beacon_xs.add(bx)

ranges.sort()
covered = 0
last_x = -inf
for x1, x2 in ranges:
  if last_x < x2:
    if last_x < x1:
      covered += x2 - x1 + 1
    else:
      covered += x2 - last_x
    last_x = x2
print(covered - len(beacon_xs))
