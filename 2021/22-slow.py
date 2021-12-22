import re
import sys

pattern = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$')

def ParseLine(line):
    '''Parses a line into tuple: ((x1, x2, y1, y2, z1, z2), bit)'''
    bit, *coords = pattern.match(line).groups()
    return (tuple(map(int, coords)), bit == 'on')

steps = [ParseLine(line) for line in sys.stdin]

def Limit(steps):
    return [
        ((max(x1, -50), min(x2, 50),
          max(y1, -50), min(y2, 50),
          max(z1, -50), min(z2, 50)),
         bit)
        for (x1, x2, y1, y2, z1, z2), bit in steps
        if x1 <= 50 and x2 >= -50 and
           y1 <= 50 and y2 >= -50 and
           z1 <= 50 and z2 >= -50]

def Solve(steps):
    xs = set()
    ys = set()
    zs = set()
    for (x1, x2, y1, y2, z1, z2), bit in steps:
        xs.add(x1)
        xs.add(x2 + 1)
        ys.add(y1)
        ys.add(y2 + 1)
        zs.add(z1)
        zs.add(z2 + 1)
    xs = sorted(xs)
    ys = sorted(ys)
    zs = sorted(zs)
    xsi = dict((x, i) for (i, x) in enumerate(xs))
    ysi = dict((y, i) for (i, y) in enumerate(ys))
    zsi = dict((z, i) for (i, z) in enumerate(zs))

    cubes = [[[False]*len(zs) for _ in range(len(ys))] for _ in range(len(xs))]
    for n, ((x1, x2, y1, y2, z1, z2), bit) in enumerate(steps):
        for i in range(xsi[x1], xsi[x2 + 1]):
            for j in range(ysi[y1], ysi[y2 + 1]):
                for k in range(zsi[z1], zsi[z2 + 1]):
                    if bit:
                        cubes[i][j][k] = True
                    else:
                        cubes[i][j][k] = False
    return sum(
        (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j]) * (zs[k + 1] - zs[k])
        for i in range(len(xs))
        for j in range(len(ys))
        for k in range(len(zs))
        if cubes[i][j][k])


print(Solve(Limit(steps)))
print(Solve(steps))
