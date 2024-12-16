from heapq import heappush, heappop
from math import inf
import sys

# Directions in clockwise order: right, down, left, up.
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Read a grid of characters.
grid = [list(line.strip()) for line in sys.stdin]
H = len(grid)
W = len(grid[0])

# Find start and end points in the grid (there should be exactly 1 of each)
start_pos = end_pos = None
for r in range(H):
    for c in range(W):
        if grid[r][c] == 'S':
            assert start_pos is None
            start_pos = (r, c)
        elif grid[r][c] == 'E':
            assert end_pos is None
            end_pos = (r, c)
assert start_pos is not None
assert end_pos is not None

# For a given vertex, generates of all neighbors with associated weights,
# as (vertex, weight) pairs.
def Adj(v):
    pos, dir = v
    r, c = pos
    dr, dc = DIRS[dir]
    r2 = r + dr
    c2 = c + dc
    assert 0 <= r2 < H and 0 <= c2 < W  # grid is surrounded by walls
    if grid[r2][c2] != '#': yield (((r2, c2), dir), 1)  # move forward
    yield ((pos, (dir - 1) % 4), 1000)  # turn left
    yield ((pos, (dir + 1) % 4), 1000)  # turn right


# Run Dijkstra's algorithm to find the shortest paths from start to finish,
# keeping track of optimal predecessors for each node, so we can construct
# all shortest parts afterwards.
#
# A vertex in the graph is a pair (pos, dir) where `pos` is a pair (row, col)
# describing a point in the grid, and `dir` a direction from 0 (right) to 3.
start = (start_pos, 0)
dist = {start: 0}
todo = [(0, start)]
pred = {start: []}
while todo:
    dist_v, v = heappop(todo)
    if dist_v > dist[v]:
        continue  # already processed before
    for w, cost in Adj(v):
        old_dist_w = dist.get(w, inf)
        new_dist_w = dist_v + cost
        if new_dist_w < old_dist_w:
            pred[w] = [v]
            dist[w] = new_dist_w
            heappush(todo, (new_dist_w, w))
        elif new_dist_w == old_dist_w:
            pred[w].append(v)

# Part 1: calculate minimum distance to end position (regardless of direciton)
min_dist = min(dist[(end_pos, dir)] for dir in range(4))
print(min_dist)

# Part 2: calculate number of positions that are part of an optimal path
optimal = set()
todo = [(end_pos, dir) for dir in range(4) if dist[(end_pos, dir)] == min_dist]
for v in todo:
    todo.extend(pred[v])
print(len(set(pos for (pos, dir) in todo)))
