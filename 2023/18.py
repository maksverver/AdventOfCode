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


def Points(segment):
  r1, c1, r2, c2 = segment
  if r1 == r2 and c1 != c2: return [(r1, c) for c in range(c1, c2, (c1 < c2) - (c1 > c2))]
  if r1 != r2 and c1 == c2: return [(r, c1) for r in range(r1, r2, (r1 < r2) - (r1 > r2))]
  assert False


def DrawDebugImage(grid):
  from PIL import Image, ImageDraw
  im = Image.new('RGB', (len(grid[0]), len(grid)), (0, 0, 0))
  draw = ImageDraw.Draw(im, 'RGB')
  colors = {
    'o': (128, 128, 128),
    '#': (255, 255, 255),
    '.': (  0,   0,   0),
  }
  for r, row in enumerate(grid):
    for c, ch in enumerate(row):
      im.putpixel((c, r), colors[ch])
  return im


def Solve(part2):
  segments = ParseSegments(part2)

  # Compress coordinates into range 2N × 2N
  rs = sorted(set(r for r1, c1, r2, c2 in segments for r in [r1, r1 + 1, r2, r2 + 1]))
  cs = sorted(set(c for r1, c1, r2, c2 in segments for c in [c1, c1 + 1, c2, c2 + 1]))
  new_rs = dict((r, i) for (i, r) in enumerate(rs))
  new_cs = dict((c, i) for (i, c) in enumerate(cs))
  segments = [(new_rs[r1], new_cs[c1], new_rs[r2], new_cs[c2]) for r1, c1, r2, c2 in segments]

  # Fill grid with boundary of trench, starting from point (1, 1) instead
  # of (0, 0) to allow space to flood fill around it.
  H = len(rs) + 1
  W = len(cs) + 1
  grid = [['.']*W for _ in range(H)]
  for segment in segments:
    for r, c in Points(segment):
      grid[r + 1][c + 1] = '#'

  # Flood fill from the outside.
  grid[0][0] = 'o'
  todo = [(0, 0)]
  while todo:
    r, c = todo.pop()
    for r2, c2 in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
      if 0 <= r2 < H and 0 <= c2 < W and grid[r2][c2] == '.':
        grid[r2][c2] = 'o'
        todo.append((r2, c2))

  if False and not part2:
    DrawDebugImage(grid).save('out.png')

  # Calculate areas of rectangles that are not on the outside, i.e., inside or
  # on the boundary.
  return sum(
      (rs[r] - rs[r - 1]) * (cs[c] - cs[c - 1])
      for r in range(H) for c in range(W) if grid[r][c] != 'o')


print(Solve(False))   # Part 1
print(Solve(True))    # Part 2
