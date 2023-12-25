# https://cses.fi/problemset/task/1671
#
# This implementation uses defaultdicts for `adj` and `dist`, which works well
# when vertices are complex objects like strings or tuples. For a slightly more
# efficient version in the case where vertices are integers, see dijkstra.py.

from collections import defaultdict
from heapq import heappush, heappop
from math import inf
import sys

# Read input
with open('dijkstra.in', 'rt') as f:
  N, M = map(int, f.readline().split())
  adj = defaultdict(list)
  for _ in range(M):
    v, w, c = map(int, f.readline().split())
    adj[v].append((w, c))

# Dijkstra's algorithm
start = 1
dist = defaultdict(lambda: inf)
dist[start] = 0
todo = [(0, start)]
while todo:
  d, v = heappop(todo)
  if d > dist[v]: continue
  for w, c in adj[v]:
    if (e := d + c) < dist[w]:
      dist[w] = e
      heappush(todo, (e, w))

print(*[dist[i] for i in range(1, N + 1)])
