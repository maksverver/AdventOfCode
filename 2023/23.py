from math import inf
import sys

grid = [list(s.strip()) for s in sys.stdin]

H = len(grid)
W = len(grid[0])

START = (0, 1)
FINISH = (H - 1, W - 2)

SLOPES = {
  '^': (-1, 0),
  '<': (0, -1),
  '>': (0, 1),
  'v': (1, 0),
}

def Solve(respect_slopes):

  # Returns the accessible neighbors of v, excluding u
  def Neighbors(v, u):
    r1, c1 = v

    if respect_slopes and (ch := grid[r1][c1]) != '.':
      dr, dc = SLOPES[ch]
      w = (r2 := r1 + dr), (c2 := c1 + dc)
      assert 0 <= r2 < H and 0 <= c2 < W and grid[r2][c2] == '.'
      return [w] * (w != u)

    return [(r2, c2)
        for (r2, c2) in [(r1 - 1, c1), (r1, c1 - 1), (r1, c1 + 1), (r1 + 1, c1)]
        if 0 <= r2 < H and 0 <= c2 < W and grid[r2][c2] != '#' and (r2, c2) != u]

  # Finds the next junction w starting from v. Returns a pair (length, w).
  def FindNextJunction(v, u):
    l = 0
    while len(ns := Neighbors(v, u)) == 1:
      u = v
      v, = ns
      l += 1
    return l, v

  # Constructs a graph in adjacency list form with integer vertices.
  #
  # The result is a list `adj` such that adj[v] contains (l, w) if there is a
  # direct path from `v` to `w` with length `l`.
  #
  # FINISH is assigned index 0, and START is assigned index 1.
  #
  def CalculateGraph():
    coords = [FINISH, START]
    index = {FINISH: 0, START: 1}
    graph = [[]]
    while len(graph) < len(coords):
      i = len(graph)
      v = coords[i]
      adj = []
      for n in Neighbors(v, None):
        l, w = FindNextJunction(n, v)
        j = index.get(w, -1)
        if j == -1:
          index[w] = j = len(coords)
          coords.append(w)
        adj.append((l + 1, j))
      graph.append(adj)
    return graph

  graph = CalculateGraph()
  memo = {}

  def FindLongestPath(v, visited):
    if v == 0: return 0  # 0=FINISH
    key = (v, visited)
    res = memo.get(key, None)
    if res is None:
      visited |= 1 << v
      res = -inf
      for l, w in graph[v]:
        if (visited & (1 << w)) == 0:
          res = max(res, l + FindLongestPath(w, visited))
      memo[key] = res
    return res

  return FindLongestPath(1, 0)  # 1=START

print(Solve(respect_slopes=True))   # Part 1
print(Solve(respect_slopes=False))  # Part 2
