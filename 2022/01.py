from heapq import heappush, heappushpop
import sys

groups = [[int(line) for line in paragraph.split()]
  for paragraph in sys.stdin.read().split("\n\n")]

# Part 1
print(max(map(sum, groups)))

# Part 2
top3 = []
for total in map(sum, groups):
  if len(top3) < 3:
    heappush(top3, total)
  else:
    heappushpop(top3, total)
print(sum(top3))
