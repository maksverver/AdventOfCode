import re
import sys

pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')

horiz = []
vert = []
diag1 = []
diag2 = []

minx = float('+inf')
maxx = float('-inf')
miny = float('+inf')
maxy = float('-inf')

for line in sys.stdin:
    x1, y1, x2, y2 = map(int, pattern.match(line).groups())
    if x1 > x2 or (x1 == x2 and y1 > y2):
        x1, y1, x2, y2 = x2, y2, x1, y1
    minx = min(minx, x1, x2)
    maxx = max(maxx, x1, x2)
    miny = min(miny, y1, y2)
    maxy = max(maxy, y1, y2)
    line = x1, y1, x2, y2
    if y1 == y2:
        horiz.append(line)
    elif x1 == x2:
        vert.append(line)
    elif y2 - y1 == x2 - x1:
        diag1.append(line)
    elif y1 - y2 == x2 - x1:
        diag2.append(line)
    else:
        assert False

def Solve():
    answer1 = 0
    answer2 = 0
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            covered = 0
            for x1, y1, x2, y2 in horiz:
                covered += y == y1 and x1 <= x <= x2
            for x1, y1, x2, y2 in vert:
                covered += x == x1 and y1 <= y <= y2
            answer1 += covered > 1
            for x1, y1, x2, y2 in diag1:
                covered += (x - x1) == (y - y1) and x1 <= x <= x2
            for x1, y1, x2, y2 in diag2:
                covered += (x - x1) == (y1 - y) and x1 <= x <= x2
            answer2 += covered > 1
    print(answer1)
    print(answer2)

Solve()
