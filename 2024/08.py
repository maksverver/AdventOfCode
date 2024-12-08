from collections import defaultdict
from math import gcd
import sys

# Read input; we only need to store antenna's locations.
antennas_by_type = defaultdict(list)
for r, line in enumerate(sys.stdin):
    for c, ch in enumerate(line.strip()):
        if ch != '.':
            antennas_by_type[ch].append((r, c))

H = r + 1
W = c + 1

def DebugPrint(points=set()):
    for r, row in enumerate(grid):
        print(''.join(('#' if (r, c) in points else ch) for c, ch in enumerate(row)))

def Part1():
    points = set()
    for positions in antennas_by_type.values():
        for r1, c1 in positions:
            for r2, c2 in positions:
                if r1 != r2 or c1 != c2:
                    dr = r2 - r1
                    dc = c2 - c1
                    assert gcd(dr, dc) == 1
                    r = r1 - dr
                    c = c1 - dc
                    if 0 <= r < H and 0 <= c < W:
                        points.add((r, c))
    #DebugPrint(points)
    return len(points)

def Part2():
    points = set()
    for positions in antennas_by_type.values():
        for r1, c1 in positions:
            for r2, c2 in positions:
                if r1 != r2 or c1 != c2:
                    dr = r2 - r1
                    dc = c2 - c1
                    assert gcd(dr, dc) == 1
                    r = r1
                    c = c1
                    while 0 <= r < H and 0 <= c < W:
                        points.add((r, c))
                        r -= dr
                        c -= dc
    #DebugPrint(points)
    return len(points)

print(Part1())
print(Part2())
