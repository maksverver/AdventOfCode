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

stack = [(0, 500)]

def DropSand(with_floor):
  r, c = stack.pop()
  while r + 1 < floor_r:
    if bitmap[r + 1][c] == '.':
      stack.append((r, c))
      r += 1
      continue
    if bitmap[r + 1][c - 1] == '.':
      stack.append((r, c))
      r += 1
      c -= 1
      continue
    if bitmap[r + 1][c + 1] == '.':
      stack.append((r, c))
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

while stack:
  DropSand(True)
  counter += 1

print(counter)
