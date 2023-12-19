import re
import sys

DIRS = {
  'R': (0, 1),
  'D': (1, 0),
  'L': (0, -1),
  'U': (-1, 0),
}

PATTERN = re.compile(r'^([URDL]) (\d+) \(#([a-f0-9]{6})\)$')

def ParseLine(line):
  direction, steps, rgb = PATTERN.match(line).groups()
  return direction, int(steps), int(rgb, 16)

# A list of (direction, steps, color) tuples
instructions = [ParseLine(line) for line in sys.stdin]


def ParseSegments(part2):
  segments = []
  r = c = 0
  for direction, steps, rgb in instructions:
    if part2:
      direction = "RDLU"[rgb % 16]
      steps = rgb // 16
    old_r = r
    old_c = c
    dr, dc = DIRS[direction]
    r += dr*steps
    c += dc*steps
    segments.append((old_r, old_c, r, c))
  assert r == c == 0
  return segments


def Solve(part2):
  segments = ParseSegments(part2)

  # Shoelace formula for the area of a simple polygon. Note: this assumes that
  # segments do not overlap or intersect (which is true for the official data).
  double_area = abs(sum(r1*c2 - r2*c1 for r1, c1, r2, c2 in segments))

  # Account for width of walls.
  for r1, c1, r2, c2 in segments:
    double_area += abs(r2 - r1) + abs(c2 - c1)

  # Plus 1 for the area of the corners.
  return double_area // 2 + 1


print(Solve(False))   # Part 1
print(Solve(True))    # Part 2
