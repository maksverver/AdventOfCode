#!/bin/env pypy3

from math import floor, ceil
from random import choice, randrange, sample, shuffle, uniform

import sys

sys.path.append('../../library-code/')

from disjointset import DisjointSet

def shuffled(iterable):
    l = list(iterable)
    shuffle(l)
    return l

debug_print = False

# Note: the final grid size will actually be (2W - 1)×(2H - 1)
#W, H = 10, 10     # testing
W, H = 51, 51   # small  (becomes 101x101)
#W, H = 251, 251   # medium (becomes 501x501)
#W, H = 1251, 1251  # large  (becomes 2501x2501)

all_edges = (
    [((r, c), (r, c + 1)) for r in range(H) for c in range(W - 1)] +
    [((r, c), (r + 1, c)) for r in range(H - 1) for c in range(W)])

vertices = [(r, c) for r in range(H) for c in range(W)]

ds = DisjointSet(vertices)

edges = set()
for e in shuffled(all_edges):
    v, w = e
    if ds.Union(v, w):
        edges.add(e)

adj = {}
for v, w in edges:
    if v not in adj: adj[v] = []
    if w not in adj: adj[w] = []
    adj[v].append(w)
    adj[w].append(v)

H = 2*H - 1
W = 2*W - 1
grid = [['#'] * W for _ in range(H)]
for v, w in edges:
    r1, c1 = v
    r2, c2 = w
    grid[2*r1][2*c1] = grid[2*r2][2*c2] = grid[r1 + r2][c1 + c2] = '.'

if debug_print:
    for row in grid:
        print(''.join(row))
    print()

start = (0, 0)
finish = (H-1, W-1)

walls  = {(r, c) for r in range(H) for c in range(W) if grid[r][c] == '#'}
spaces = {(r, c) for r in range(H) for c in range(W) if grid[r][c] == '.'}

def Neighbors(v):
    r, c = v
    return [(r2, c2) for (r2, c2) in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)] if 0 <= r2 < H and 0 <= c2 < W]

def ShortestPath():
    todo = [(start, 0)]
    dist = {start: 0}
    for v, d in todo:
        if v == finish:
            path = [finish]
            while v != start:
                d -= 1
                v, = (w for w in Neighbors(v) if w not in walls and dist.get(w) == d)
                path.append(v)
            assert d == 0
            return reversed(path)
        for w in Neighbors(v):
            if w not in walls and w not in dist:
                dist[w] = d + 1
                todo.append((w, d + 1))

on_path = set(ShortestPath())
other = spaces - on_path

assert len(walls) + len(other) + len(on_path) == H * W

if debug_print:
    for r in range(H):
        print(''.join(
            ('#' if (r, c) in walls else
            'O' if (r, c) in on_path else
            '.') for c in range(W)))
    print()

points = shuffled(walls) + shuffled(other) + shuffled(on_path)
for r, c in points:
     print(c, r, sep=',')

# Expected answers:
t = len(walls) + len(other)
r, c = points[t]
print('t', t, sep='=', file=sys.stderr)
print(c, r, sep=',', file=sys.stderr)
