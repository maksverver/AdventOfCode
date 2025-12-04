#!/usr/bin/env python3

from random import uniform

def GenRandom(H, W, p, f):
    for _ in range(H):
        print(''.join('.@'[uniform(0, 1) < p] for _ in range(W)), file=f)

def Rot180(grid):
    x = len(grid)
    assert all(len(row) == x for row in grid)
    return [[grid[-i - 1][-j - 1] for j in range(x)] for i in range(x)]

def GenSpiral(N, f):
    n = 2
    grid = [['@']*2]*2
    for _ in range(N):
        grid = Rot180(grid)
        n += 4
        grid = (
            [['.']*(n-2) + ['@']*2]*2 +
            [row + ['.', '.', '@', '@'] for row in grid] +
            [['@']*n]*2
        )
    for row in grid:
        print(''.join(row), file=f)


if 0:
    with open('challenge-1.txt', 'wt') as f:
        GenRandom(400, 300, 2/3, f)

    with open('challenge-2.txt', 'wt') as f:
        GenRandom(1000, 1500, 2/3, f)

    with open('challenge-3.txt', 'wt') as f:
        GenSpiral(100, f)
