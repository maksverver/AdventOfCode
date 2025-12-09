from math import prod
import sys

class DisjointSet:
    def __init__(self, members):
        self.parents = {k: k for k in members}
        self.sizes = {k: 1 for k in members}

    def Find(self, x):
        if (root := self.parents[x]) != x:
            root = self.parents[x] = self.Find(root)
        return root

    def Union(self, x, y):
        x = self.Find(x)
        y = self.Find(y)
        if x == y: return False
        if self.sizes[x] < self.sizes[y]: x, y = y, x
        self.sizes[x] += self.sizes[y]
        self.parents[y] = x
        del self.sizes[y]
        return True

    def Size(self, x):
        return self.sizes[self.Find(x)]


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
