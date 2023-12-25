# https://cses.fi/problemset/task/1671
#
# This implementation uses flat lists for `adj` and `dist`, which works well
# when vertices are integers (ideally starting from 0). For the case where
# vertices are more complex (e.g. strings or tuples) see dijkstra2.py.

from heapq import heappush, heappop
from math import inf
import sys

# Read input
with open('dijkstra.in', 'rt') as f:
  N, M = map(int, f.readline().split())
  adj = [[] for _ in range(N)]
  for _ in range(M):
    v, w, c = map(int, f.readline().split())
    adj[v - 1].append((w - 1, c))

# Dijkstra's algorithm
start = 0
dist = [inf]*N
dist[start] = 0
todo = [(0, start)]
while todo:
  d, v = heappop(todo)
  if d > dist[v]: continue
  for w, c in adj[v]:
    if (e := d + c) < dist[w]:
      dist[w] = e
      heappush(todo, (e, w))

print(*dist)
