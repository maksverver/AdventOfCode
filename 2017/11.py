import sys

dirs = {
    'n':  (-1, -1),
    'ne': ( 0, -1),
    'nw': (-1,  0),
    'se': (+1,  0),
    'sw': ( 0, +1),
    's':  (+1, +1),
}

def Dist(x, y):
    return max(abs(x), abs(y))

max_dist = 0
x, y = 0, 0
for step in sys.stdin.readline().strip().split(','):
    dx, dy = dirs[step]
    x += dx
    y += dy
    max_dist = max(max_dist, Dist(x, y))
print(Dist(x, y))
print(max_dist)
