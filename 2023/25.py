from collections import defaultdict
import sys
from random import sample

def DebugDumpGraphViz(filename):
  with open(filename,'wt') as f:
    print('graph {', file=f)
    for v in adj:
      for w in adj[v]:
        if v <= w:
          print(v, '--', w, file=f)
    print('}', file=f)

def ParseGraph(file):
  adj = defaultdict(set)
  for line in file:
    v, ws = line.split(': ')
    for w in ws.split():
      assert v not in adj[w]
      assert w not in adj[v]
      adj[v].add(w)
      adj[w].add(v)
  return adj

# Read input
adj = ParseGraph(sys.stdin)

sys.setrecursionlimit(len(adj) + 100)

# DebugDumpGraphViz('out.gv')

def MinCut(start, finish):
  edges_used = set()

  def Augment():
    visited = set()
    def Dfs(v):
      if v == finish:
        return True
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
  while Augment():
    min_cut += 1

  def GetMinCutEdges():
    visited = set()
    def Dfs(v):
      visited.add(v)
      assert v != finish
      for w in adj[v]:
        if w not in visited and (v, w) not in edges_used:
          Dfs(w)
    Dfs(start)
    return [(v, w) for v in visited for w in adj[v] if w not in visited]

  edges = GetMinCutEdges()
  assert len(edges) == min_cut
  return edges


def FindComponents(omit_edges):
  components = []
  visited = set()
  todo = []
  for start in adj:
    if start not in visited:
      component = set([start])
      todo.append(start)
      while todo:
        v = todo.pop()
        assert v not in visited
        visited.add(v)
        for w in adj[v]:
          assert v != w
          if w not in component and (v, w) not in omit_edges and (w, v) not in omit_edges:
            component.add(w)
            todo.append(w)
      components.append(component)
  assert sum(map(len, components)) == len(adj)
  return components

# Solve
while True:
  edges = MinCut(*sample(list(adj), k=2))
  if len(edges) == 3:
    break
  assert len(edges) > 3
a, b = FindComponents(edges)
print(len(a) * len(b))
