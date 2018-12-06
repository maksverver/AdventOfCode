from collections import Counter
import sys

size = 1000
coords = [tuple(map(int, line.strip().split(','))) for line in sys.stdin]

def Part1():
  counts = Counter()
  infinite = set()
  for x in range(size):
    for y in range(size):
      min_dist = None
      closest_i = None
      for i, (xx, yy) in enumerate(coords):
        dist = abs(x - xx) + abs(y - yy)
        if min_dist is None or dist < min_dist:
          min_dist = dist
          closest_i = i
        elif dist == min_dist:
          closest_i = None
      if closest_i is not None:
        if x == 0 or x == size - 1 or y == 0 or y == size - 1:
          infinite.add(closest_i)
        counts[closest_i] += 1
  for i in infinite:
    del counts[i]
  (_, count), = counts.most_common(1)
  return count

def Part2():
  count = 0
  for x in range(size):
    for y in range(size):
      dist = 0
      for xx, yy in coords:
        dist += abs(xx - x) + abs(yy - y)
        if dist >= 10000:
          break
      else:
        count += 1
  return count

print(Part1())
print(Part2())
