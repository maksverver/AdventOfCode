from hashlib import md5
import sys

password = sys.stdin.readline().strip()
queue = [(0, 0, '')]
for r, c, path in queue:
  if (r, c) == (3, 3):
    longest_path = path
    continue
  doors = [ch > 'a' for ch in md5(bytes(password + path, 'ascii')).hexdigest()[:4]]
  for door, dir, r2, c2 in zip(doors, "UDLR", (r - 1, r + 1, r, r), (c, c, c - 1, c + 1)):
    if door and 0 <= r2 < 4 and 0 <= c2 < 4:
      queue.append((r2, c2, path + dir))
print(len(longest_path))
