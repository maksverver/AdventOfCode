# Variant of 14.py that doesn't use a stack to accelerate DropSand().
# In theory this should be significantly slower. In practice, it's somewhat
# slower with CPython but not with pypy3.

import sys

H = 1000
W = 1000
bitmap = [['.']*H for _ in range(W)]

floor_r = 0

for line in sys.stdin:
  coords = [tuple(map(int, part.split(','))) for part in line.strip().split(' -> ')]
  for i in range(len(coords) - 1):
    (c1, r1), (c2, r2) = coords[i:i + 2]
    if r1 > r2: r1, r2 = r2, r1
    if c1 > c2: c1, c2 = c2, c1
    for r in range(r1, r2 + 1):
      for c in range(c1, c2 + 1):
        bitmap[r][c] = '#'
    floor_r = max(floor_r, r1 + 2)

def DropSand(with_floor):
  r, c = 0, 500
  while r + 1 < floor_r:
    if bitmap[r + 1][c] == '.':
      r += 1
      continue
    if bitmap[r + 1][c - 1] == '.':
      r += 1
      c -= 1
      continue
    if bitmap[r + 1][c + 1] == '.':
      r += 1
      c += 1
      continue
    break
  if r + 1 < floor_r or with_floor:
    bitmap[r][c] = 'o'
    return True
  return None

counter = 0
while DropSand(False):
  counter += 1

print(counter)

while bitmap[0][500] == '.':
  DropSand(True)
  counter += 1

print(counter)
