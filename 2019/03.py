import sys

def Parse(line):
    dirs = {
        'R': ( 0, +1),
        'L': ( 0, -1),
        'U': (+1,  0),
        'D': (-1,  0),
    }
    r, c = 0, 0
    steps = 0
    points = {}
    for part in line.split(','):
        dr, dc = dirs[part[0]]
        dist = int(part[1:])
        for _ in range(dist):
            r += dr
            c += dc
            steps += 1
            if (r, c) not in points:
                points[r, c] = steps
    return points

points1 = Parse(sys.stdin.readline())
points2 = Parse(sys.stdin.readline())

intersections = set(points1).intersection(set(points2))

print(min(abs(r) + abs(c) for r, c in intersections))
print(min(points1[p] + points2[p] for p in intersections))
