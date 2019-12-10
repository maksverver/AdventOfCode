from math import gcd
import sys

positions = []
for y, line in enumerate(sys.stdin):
    for x, ch in enumerate(line):
        if ch == '#':
            positions.append((x, y))

def CountVisible(x1, y1):
    visible = set()
    for x2, y2 in positions:
        if (x1, y1) == (x2, y2):
            continue
        dx = x2 - x1
        dy = y2 - y1
        n = gcd(dx, dy)
        dx //= n
        dy //= n
        visible.add((dx, dy))
    return len(visible)

cx, cy = max(positions, key=lambda xy: CountVisible(*xy))
print(CountVisible(cx, cy))
