#!/usr/bin/env pypy3

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


def FindSegmentsAtY(target_y):
  # Calculate horizontal segments covered by sensors
  segments = []
  for x, y, r in sensors:
    dx = r - abs(y - target_y)
    if dx >= 0:
      segments.append((x - dx, x + dx))

  # Merge overlapping/touching segments
  result = []
  if len(segments) > 0:
    segments.sort()
    cur_x1, cur_x2 = segments[0]
    for x1, x2 in segments[1:]:
      assert x1 >= cur_x1
      if cur_x2 + 1 < x1:
        # Found a gap; start a new segment
        result.append((cur_x1, cur_x2))
        cur_x1, cur_x2 = x1, x2
      elif cur_x2 < x2:
        # Extend existing segment
        cur_x2 = x2
    result.append((cur_x1, cur_x2))
  return result


def SolvePart1(target_y):
  covered = sum(x2 - x1 + 1 for x1, x2 in FindSegmentsAtY(target_y))
  beacon_xs = set(x for x, y in beacons if y == target_y)
  return covered - len(beacon_xs)

def SolvePart2(max_x, max_y):
  answer = None
  for y in range(max_y + 1):
    segments = FindSegmentsAtY(y)
    if len(segments) == 1:
      # In theory it's possible for the missing beacon to be located at
      # the edge of the search space, but it probably isn't.
      assert segments[0][0] <= 0 and segments[0][1] >= max_x
    else:
      assert len(segments) == 2
      assert segments[1][0] - segments[0][1] == 2
      assert answer is None
      x = segments[0][1] + 1
      answer = 4000000 * x + y
  return answer

print(SolvePart1(2000000))
print(SolvePart2(4000000, 4000000))
