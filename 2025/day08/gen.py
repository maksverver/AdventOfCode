#!/usr/bin/env python3

from random import randint, shuffle
import sys

def GenCase(N, w1, w2, w3, o1, o2, o3, max_dist, filename):

    def Dist3D(pair):
        (x1, y1, z1), (x2, y2, z2) = pair
        return (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2

    def GenPoint():
        return (
            randint(1, w1) + o1*randint(0, 1),
            randint(1, w2) + o2*randint(0, 1),
            randint(1, w3) + o3*randint(0, 1),
        )

    points = []
    distances = set()
    while len(points) < N:
        p = GenPoint()
        dists = {Dist3D((p, q)) for q in points}
        if len(dists) == len(points) and 0 not in dists and not (distances & dists):
            distances.update(dists)
            points.append(p)

    # Check points are distinct
    assert len(set(points)) == len(points)

    # Check distances are distinct
    pairs = {Dist3D((p, q)) for p in points for q in points if p < q}
    assert len(pairs) == N*(N - 1)//2

    assert max(distances) < max_dist

    shuffle(points)  # unnecessary?
    with open(filename, 'wt') as f:
        for p in points:
            print(*p, sep=',', file=f)

# Squared distances fit in 32-bit integers
if 0:
    GenCase(1000, 10000, 10000, 10000, 20000, 0, 0, 2**31, 'challenge-1.txt')

# Squared distances fit in doubles or 64-bit integers
if 0:
    GenCase(10000, 10**6, 10**6, 10**6, 0, 10**7, 0, 2**50, 'challenge-2.txt')

if 0:
    # Generate a case where the nearest point alternates between a center
    # point. It's 2D version of:
    #
    #   o---o---o---o---0---o---o---o---o
    #     8   6   4   2   1   3   5   7
    #
    # This is supposed to defeat inefficient set merging algorithms, but in
    # reality it doesn't matter because the pair sorting part of the solution
    # takes O(N^2) time anyway, so even suboptimal merging algorithms don't
    # change the overall complexity.
    dist_sqs = set()
    steps = []
    for dx in range(1, 150):
        for dy in range(1, 150):
            d = dx**2 + dy**2
            if d not in dist_sqs:
                dist_sqs.add(d)
                steps.append((dx, dy))
    steps.sort(key=lambda v: sum(x**2 for x in v))
    points = [(0, 0)]
    lx = ly = rx = ry = 0
    for i, (dx, dy) in enumerate(steps):
        if i % 2 == 0:
            rx += dx
            ry += dy
            points.append((rx, ry))
        else:
            lx -= dx
            ly -= dy
            points.append((lx, ly))
    shuffle(points)
    for x, y in points:
        print(x - lx + 1, y - ly + 1, 42, sep=',')
