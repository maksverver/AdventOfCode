# A version of 25.py that has been minimized by removing unnecessary functions
# and assertions. Shorter, but less clear.

from collections import defaultdict
import sys
from random import shuffle

adj = defaultdict(set)
for line in sys.stdin:
  v, ws = line.split(': ')
  for w in ws.split():
    adj[v].add(w)
    adj[w].add(v)

sys.setrecursionlimit(len(adj)*3 + 100)   # *3 needed for PyPy

vertices = list(adj)
shuffle(vertices)
start, *rest = vertices
for finish in rest:
  edges_used = set()

  def Augment():
    visited = set()
    def Dfs(v):
      if v == finish: return True
      visited.add(v)
      for w in adj[v]:
        if w not in visited and (v, w) not in edges_used and Dfs(w):
          if (w, v) in edges_used:
            edges_used.remove((w, v))
          else:
            edges_used.add((v, w))
          return True
      return False
    return Dfs(start)

  min_cut = 0
  while min_cut <= 3 and Augment():
    min_cut += 1

  if min_cut == 3: break

visited = set()
def Dfs(v):
  visited.add(v)
  for w in adj[v]:
    if w not in visited and (v, w) not in edges_used: Dfs(w)
Dfs(start)
print(len(visited) * (len(adj) - len(visited)))
