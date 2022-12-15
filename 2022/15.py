from math import inf
import re
import sys

def ParseLine(line):
  m = re.match('^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$', line)
  sx, sy, bx, by = map(int, m.groups())
  return (sx, sy, bx, by)

sensors = []
beacons = []

for sx, sy, bx, by in map(ParseLine, sys.stdin):
  sensors.append((sx, sy, abs(bx - sx) + abs(by - sy)))
  beacons.append((bx, by))

def SolvePart1(target_y):
  # Calculate horizontal segments intersecting target_y
  segments = []
  for x, y, r in sensors:
    dx = r - abs(y - target_y)
    if dx >= 0:
      segments.append((x - dx, x + dx))
  # Count total distance covered by segments, ignoring overlap
  segments.sort()
  covered = 0
  last_x = -inf
  for x1, x2 in segments:
    if last_x < x2:
      if last_x < x1:
        covered += x2 - x1 + 1
      else:
        covered += x2 - last_x
      last_x = x2
  # Remove beacons themselves from the count (they necessarily overlap)
  beacon_xs = set(x for x, y in beacons if y == target_y)
  return covered - len(beacon_xs)

def IsCovered(bx, by):
  for sx, sy, r in sensors:
    if abs(sx - bx) + abs(sy - by) <= r:
      return True
  return False

def SolvePart2(max_x, max_y):
  # The beacon must lie just outside the boundary of a sensor's range.
  # Unless the beacon lies on a boundary of the grid (0, 0)-(max_x,max_y)
  # (which seems unlikely), it must lie on the intersection of at least two
  # sensor's boundaries, so calculate these intersection points.
  diags1 = []  # x increasing, y increasing
  diags2 = []  # x increasing, y decreasing
  for x, y, r in sensors:
    diags1.append((x, y - r - 1, x + r + 1, y))
    diags1.append((x - r - 1, y, x, y + r + 1))
    diags2.append((x - r - 1, y, x, y - r - 1))
    diags2.append((x, y + r + 1, x + r + 1, y))
  candidates = set()
  for d1x1, d1y1, d1x2, d1y2 in diags1:
    for d2x1, d2y1, d2x2, d2y2 in diags2:
      # calculate intersection point via x-axis intersection
      x1 = (d1x1 - d1y1)
      x2 = (d2x1 + d2y1)
      d = x2 - x1
      if d % 2 != 0: continue  # not on integer point
      y = d // 2
      x = x1 + y
      assert x == x2 - y
      if (max(0, d1x1, d2x1) <= x <= min(max_x, d1x2, d2x2) and
          max(0, d1y1, d2y2) <= y <= min(max_y, d1y2, d2y1)):
        candidates.add((x, y))

  # Find the only candidate that is not covered by any sensors:
  answer, = (4000000 * x + y for x, y in candidates if not IsCovered(x, y))
  return answer

print(SolvePart1(2000000))
print(SolvePart2(4000000, 4000000))
