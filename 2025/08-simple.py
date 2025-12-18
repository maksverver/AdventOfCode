# Simpler solution to day 8 that does not use a Disjoint Set datastructure.
# This isn't actually much slower in practice, because the time complexity is
# dominated by the O(n^2 log n) time needed to generate and sort all pairs of
# points.

from itertools import combinations
from collections import Counter
from math import prod
import sys

def ParseLine(line):
    x, y, z = map(int, line.split(','))
    return (x, y, z)

def Dist3D(pair):
    (x1, y1, z1), (x2, y2, z2) = pair
    return (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2


points = [ParseLine(line) for line in sys.stdin]
pairs = list(combinations(points, 2))
pairs.sort(key=Dist3D)
groups = {p: p for p in points}
last_pair = None
for i, (v, w) in enumerate(pairs):
    if i == 1000:
        # Part 1: product of sizes of 3 largest components after 1000 iterations
        print(prod(count for _, count in Counter(groups.values()).most_common(3)))

    a = groups[v]
    b = groups[w]
    if a != b:
        last_pair = v, w
        for u, c in groups.items():
            if c == b:
                groups[u] = a

# Part 2: product of x coordinates of last pair connected
assert last_pair is not None
print(prod(p[0] for p in last_pair))
