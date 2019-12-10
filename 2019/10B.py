from collections import defaultdict
from math import atan2, hypot, pi
import sys

positions = []
for y, line in enumerate(sys.stdin):
    for x, ch in enumerate(line):
        if ch == '#':
            positions.append((x, y))

def Angle(dx, dy):
    angle = atan2(dx, -dy)
    if angle < 0:
        angle += 2*pi
    return angle

def Arrange(x1, y1):
    '''Returns a dict of lists of positions, such that arranged[angle] contains
       the list of positions that are at the given angle (in radians) relative
       to (x1, y1), sorted by increasing distance from (x1, y1).'''
    arranged = defaultdict(list)
    for x2, y2 in positions:
        if (x1, y1) == (x2, y2):
            continue
        arranged[Angle(x2 - x1, y2 - y1)].append((x2, y2))
    for asteroids in arranged.values():
        asteroids.sort(key=lambda xy: hypot(xy[0] - x1, xy[1] - y1))
    return arranged

def FindDestroyed(cx, cy, k):
    arranged = Arrange(cx, cy)
    while arranged:
        for angle in sorted(arranged.keys()):
            positions = arranged[angle]
            k -= 1
            if k == 0:
                return positions[0]
            del positions[0]
            if not positions:
                del arranged[angle]

cx, cy = max(positions, key=lambda xy: len(Arrange(*xy)))
dx, dy = FindDestroyed(cx, cy, 200)
print(100*dx + dy)
