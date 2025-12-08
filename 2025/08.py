from math import prod
import sys

sys.path.append('../library-code')  # hack
from disjointset import DisjointSet

def ParseLine(line):
    x, y, z = map(int, line.split(','))
    return (x, y, z)

def Dist3D(pair):
    (x1, y1, z1), (x2, y2, z2) = pair
    return (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2

points = [ParseLine(line) for line in sys.stdin]
pairs = [(p, q) for i, p in enumerate(points) for q in points[i + 1:]]
pairs.sort(key=Dist3D)
ds = DisjointSet(points)
for i, (p, q) in enumerate(pairs):
    if i == 1000:
        # Part 1: product of sizes of 3 largest components after 1000 iterations
        sizes = [ds.Size(p) for p in points if ds.Find(p) == p]
        sizes.sort()
        print(prod(sizes[-3:]))

    ds.Union(p, q)

    if ds.Size(p) == len(points):
        # Part 2: product of x coordinates of last pair connected
        print(p[0] * q[0])
        break
