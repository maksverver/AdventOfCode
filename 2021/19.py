import re
import sys

mone = [
    [  1,  0,  0, ],
    [  0,  1,  0, ],
    [  0,  0,  1, ],
]

rotx = [
    [  1,  0,  0 ],
    [  0,  0,  1 ],
    [  0, -1,  0 ],
]

roty = [
    [  0,  0,  1 ],
    [  0,  1,  0 ],
    [ -1,  0,  0 ],
]

rotz = [
    [  1,  0,  0 ],
    [  0,  0,  1 ],
    [  0, -1,  0 ],
]

# Calculate all possible rotations in 3D space.
rotations = [mone]
for t in rotations:
    for u in (rotx, roty, rotz):
        # 3x3 matrix multiplication
        v = [[sum(t[i][k] * u[k][j] for k in range(3)) for i in range(3)] for j in range(3)]
        if v not in rotations:
            rotations.append(v)
assert len(rotations) == 24


def TransformPoint(p, m):
    return tuple(sum(m[i][k] * p[k] for k in range(3)) for i in range(3))

def AddPoint(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])

def SubtractPoint(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])

def ManhattanDistance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2])

def TryAlign(points1, points2):
    '''Tries to aligns points2 to points1 using rotations and translations.
       Returns a pair of: points2 transformed to the coordinates of points1,
       and a point representing the translation.'''
    for rotate in rotations:
        points3 = [TransformPoint(p, rotate) for p in points2]  # rotated
        for p1 in points1:
            for p2 in points3:
                translate = SubtractPoint(p1, p2)
                points4 = [AddPoint(p, translate) for p in points3]  # rotated + translated
                overlap_size = len(points1) + len(points4) - len(set(points1 + points4))
                if overlap_size >= 12:
                    return points4, translate

# Read input
scanned_points = []  # [[(x,y,z)]]
parts = sys.stdin.read().strip().split('\n\n')
for i, part in enumerate(parts):
    lines = part.split('\n')
    assert lines[0] == f'--- scanner {i} ---'
    points = [tuple(map(int, line.split(','))) for line in lines[1:]]
    assert len(points) == len(set(points))  # no duplicates
    scanned_points.append(points)

# Calculate positions of scanners, and points transformed to the origin
positions = [None]*len(scanned_points)
fixed_points = [None]*len(scanned_points)

# Arbitrarily define scanner 0 to be at the origin.
positions[0] = (0, 0, 0)
fixed_points[0] = scanned_points[0]

# Breadth-first search for connected points
todo = [0]
for i in todo:
    for j, points in enumerate(fixed_points):
        if points is None:
            result = TryAlign(fixed_points[i], scanned_points[j])
            if result is None:
                continue
            fixed_points[j], positions[j] = result
            todo.append(j)
assert(all(fixed_points))

# Part 1: total number of distinct points
print(len(set(p for ps in fixed_points for p in ps)))

# Part 2: greatest distance between a pair of scanners
print(max(ManhattanDistance(p, q) for p in positions for q in positions))
