import sys
import md5

dirs = {
  'U': (-1, 0),
  'D': (+1, 0),
  'L': (0, -1),
  'R': (0, +1),
}

password = sys.stdin.readline().strip()
queue = [(0, 0, '')]
for r, c, path in queue:
  if (r, c) == (3, 3):
    break
  doors = [ch > 'a' for ch in md5.new(password + path).hexdigest()[:4]]
  for door, dir, r2, c2 in zip(doors, "UDLR", (r - 1, r + 1, r, r), (c, c, c - 1, c + 1)):
    if door and 0 <= r2 < 4 and 0 <= c2 < 4:
      queue.append((r2, c2, path + dir))
print path
