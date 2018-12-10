import re
import sys

pattern = re.compile(r'position=< *(-?\d*), *(-?\d*)> velocity=< *(-?\d*), *(-?\d*)>')
stars = [tuple(map(int, pattern.match(line).groups())) for line in sys.stdin]

def GetPointsAt(t):
    return [(px + vx*t, py + vy*t) for (px, py, vx, vy) in stars]

def GetBoundingBoxAt(t):
    points = GetPointsAt(t)
    x = min(x for (x, y) in points)
    y = min(y for (x, y) in points)
    w = max(x for (x, y) in points) - x + 1
    h = max(y for (x, y) in points) - y + 1
    return (x, y, w, h)

def GetBoundingBoxSizeAt(t):
    _, _, w, h = GetBoundingBoxAt(t)
    return w*h

def GetImageAt(t):
    x, y, w, h = GetBoundingBoxAt(t)
    image = [['.']*w for _ in range(h)]
    for xx, yy in GetPointsAt(t):
        image[yy - y][xx - x] = '#'
    return [''.join(row) for row in image]

a = 0
b = 1
while GetBoundingBoxSizeAt(b - 1) >= GetBoundingBoxSizeAt(b):
    b *= 2
while a < b:
    aa = (a + a + b)//3
    bb = (a + b + b)//3
    if GetBoundingBoxSizeAt(aa) > GetBoundingBoxSizeAt(bb):
        a = aa + 1
    else:
        b = bb

# Part 1 (manual OCR required)
for row in GetImageAt(a):
    print(row)

# Part 2
print(a)
