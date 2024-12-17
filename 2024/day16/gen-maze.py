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

W, H = 20, 20     # testing 
#W, H = 100, 100   # small 
#W, H = 500, 500   # medium
#W, H = 2500, 2500  # large

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

def FindLongestPath(start):
    # TODO: count number of turns?
    dist = {start: 0}
    todo = [start]
    for v in todo:
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                todo.append(w)

    max_dist = max(dist.values())
    w = choice([v for v, d in dist.items() if d == max_dist])
    path = [w]
    while w != start:
        preds = [u for u in adj[w] if dist[u] == dist[w] - 1]
        w = choice(preds)
        path.append(w)
    assert len(path) == max_dist + 1
    return path

long_path = []
for v in sample(vertices, 100):
    path = FindLongestPath(v)
    if len(path) > len(long_path):
        long_path = path
print('Long path length:', len(long_path), file=sys.stderr)

on_path = set(long_path)

# Identify vertices that do not lie on the main path.
off_path_roots = [w for v in on_path for w in adj[v]
        if (min(v, w), max(v, w)) in edges and w not in on_path]

branch = {}
for v in long_path: branch[v] = 0

for i, root in enumerate(off_path_roots, start=1):
    todo = [root]
    seen = {root}
    for v in todo:
        for w in adj[v]:
            if w not in seen and w not in on_path:
                seen.add(w)
                todo.append(w)
    for v in todo:
        assert v not in branch
        branch[v] = i

# Add about a quarter of interior edges to create some loops outside the main path:
remaining_edges = set(all_edges) - set(edges)
for e in remaining_edges:
    v, w = e
    if 0 < branch[v] == branch[w] and uniform(0, 1) < 0.25:
        edges.add(e)

#edges = list(zip(long_path[:-1], long_path[1:]))

# Finally build the grid:
grid = [['#'] * (2*W + 1) for _ in range(2*H + 1)]
for v, w in edges:
    r1, c1 = v
    r2, c2 = w
    grid[2*r1+1][2*c1+1] = grid[2*r2+1][2*c2+1] = grid[r1 + r2 + 1][c1 + c2 + 1] = '.'

grid[1 + 2*long_path[ 0][0]][1 + 2*long_path[ 0][1]] = 'S'
grid[1 + 2*long_path[-1][0]][1 + 2*long_path[-1][1]] = 'E'

for row in grid:
    print(''.join(row))

print(len(long_path) * 2 - 1, file=sys.stderr)  # part 2 answer
