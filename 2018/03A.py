import re
import sys

overlap = [[0]*1000 for _ in range(1000)]
for line in sys.stdin:
    x1, y1, w, h = map(int, re.match(r'#\d+ @ (\d+),(\d+): (\d+)x(\d+)', line).groups())
    for x in range(x1, x1 + w):
        for y in range(y1, y1 + h):
            overlap[x][y] += 1
print(sum(x > 1 for row in overlap for x in row))
