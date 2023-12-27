from collections import defaultdict
from random import shuffle
import sys

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

# Finds a cut of size 3 between the vertices `start` and `finish`, or returns
# None if the minimum cut is greater than 3. Runs in O(E) worst-case.
def MinCut(adj, start, finish):
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
    if min_cut > 3: return None

  assert min_cut == 3

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


def FindComponents(adj, omit_edges):
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

# From the problem statement, we know that the graph can be partitioned into two
# parts, A and B, that are connected by only 3 edges.
#
# This funciton finds a cut of size 3 between part A and B by first picking a
# random start and finish vertex and then calculating the minimum cut between
# those two vertices. If the size of the minimum cut is greater than 3, then
# start and finish must lie in the same part (A or B) and we retry with a
# different vertex. This takes an expected |A|/|B| + |B|/|A| attempts, or
# max(|A|, |B|) attempts in the worst-case.
#
# Since the runtime of MinCut() is O(E) this gives a time complexity of O(VE)
# worst-case, and O((A/B + B/A)×E) expected, which means the solution is most
# efficient when A and B are approximately the same size, so that A/B + B/A is
# close to 2, and performs worse when e.g. A=1 and B is very large.
#
def FindCut(adj):
  vertices = list(adj)
  shuffle(vertices)
  start, *rest = vertices
  for finish in rest:
    edges = MinCut(adj, start, finish)
    if edges is not None: return edges
  assert False  # no solution found!

def Solve():
  adj = ParseGraph(sys.stdin)
  sys.setrecursionlimit(len(adj) + 100)
  a, b = FindComponents(adj, FindCut(adj))
  return len(a) * len(b)

if __name__ == '__main__':
  print(Solve())
