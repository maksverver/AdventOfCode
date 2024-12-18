from collections import defaultdict
from math import inf
import sys

coords = [tuple(map(int, line.split(','))) for line in sys.stdin]

H = max(r for r, c in coords) + 1
W = max(c for r, c in coords) + 1

start = (0, 0)
finish = (H - 1, W - 1)

# until[r, c] == time at which (r, c) becomes blocked
until = defaultdict(lambda: inf)
for i, (x, y) in enumerate(coords):
    until[y, x] = i


def Neighbors(v):
    r, c = v
    return [(r2, c2) for (r2, c2) in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)] if 0 <= r2 < H and 0 <= c2 < W]


def ShortestPath(t):
    todo = [(start, 0)]
    seen = {start}
    for v, d in todo:
        if v == finish:
            return d
        for w in Neighbors(v):
            if w not in seen and until[w] > t:
                seen.add(w)
                todo.append((w, d + 1))
    return inf


# Part 1: shortest path at t=1024
print(ShortestPath(1024))


# Part 2: binary search for the earliest time where there is no path
lo = 0
hi = len(coords)
while lo < hi:
    t = (lo + hi) // 2
    if ShortestPath(t) < inf:
        lo = t + 1
    else:
        hi = t
print(*coords[lo], sep=',')
