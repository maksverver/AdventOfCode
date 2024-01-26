# Solution to day 25 using the Stoer–Wagner algorithm.
#
# We are given a connected undirected graph G, and we want to find a minimum
# cut in the graph.
#
# The Stoer-Wagner algorithm is based on the idea that if we have a pair of
# vertices (s, t) and know the size of the minimum cut between s and t, then the
# minimum cut in the global graph is either that minimum cut, or the minimum cut
# in the graph obtained my merging s and t, because if the s-t min-cut is not
# globally minimal, than s and t must lie on the same side of the global
# min-cut, so we can merge them.
#
# We can find a single pair (s, t) and the associated minimum cut by starting
# from an arbitrary vertex v, repeatedly merging it with the vertex w that has
# the most edges (v, w) (note that duplicate edges will appear due to merging,
# even if they didn't occur in the input graph). The last two vertices merged
# are a pair (s, t) and the minimum cut between s and t is the number of edges
# just before merging the last vertex. (This is a nonobvious result that is
# proven in the original paper.)
#
# The above algorithm is implemented by MinimumCutPhase(). The original Stoer-
# Wagner algorithm simply runs the above algorithm V - 1 times, merging s-t
# after each step, and then taking the minimum cut found over all iterations.
#
# For the Advent of Code problem, we need to make two adjustments:
#
#  1. We need track the size of the set of vertices that each merged vertex
#     represents, which we need to calculate the final answer.
#
#  2. We can stop as soon as MinimumCutPhase() returns a min-cut of size 3,
#     which we know is minimal. (Though this doesn't improve the worst-case
#     complexity.)
#
# Since MinimumCutPhase() runs in time O(E log E) and is at most V - 1 times,
# the overall time complexity is O(V×E log E). This is worse than the max-flow
# based implementation (see 25.py), and also slower in practice on some of the
# harder inputs. Stoer-Wagner would be more efficient in the general case where
# edges can have arbitrary weight and the minimum cut is larger.
#
# References:
#
#  - https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
#  - https://dl.acm.org/doi/abs/10.1145/263867.263872

from collections import defaultdict
from heapq import heappop, heappush
import sys


# Parses graph into a list of adjacency lists. adj[v] == pairs (w, k) so that
# there are exactly k edges between (v, w).
def ParseInput(file):
  adj = []
  vertex_by_name = {}

  def GetVertex(name):
    v = vertex_by_name.get(name, None)
    if v is None:
      vertex_by_name[name] = v = len(adj)
      adj.append([])
    return v

  for line in file:
    a, bs = line.split(': ')
    v = GetVertex(a)
    for b in bs.split():
      w = GetVertex(b)
      adj[v].append(w)
      adj[w].append(v)
  return adj


# Finds a pair (s, t) so that the min-cut between them is the partition of V
# into V\{t} and {t}, and returns (s, t, min_cut).
#
# This runs in O(V + E log E) time.
def MinimumCutPhase(adj):
  assert len(adj) >= 2
  added = [False]*len(adj)
  weight = [0]*len(adj)
  queue = [(0, v) for v in range(len(adj))]
  s = t = None
  while queue:
    _, v = heappop(queue)
    if added[v]: continue
    added[v] = True
    s, t = t, v
    for w in adj[v]:
      if not added[w]:
        weight[w] += 1
        heappush(queue, (-weight[w], w))
  return s, t, weight[t]


# Returns new adjacency lists corresponding with the graph where s and t are
# merged, and edges between s and t are removed. Specifically, index s becomes
# the merged vertex, and t is removed, while vertices v > t are shifted down
# one space to fill the gap.
#
# Runs in O(V + E) time.
def Merge(adj, s, t):
  assert 0 <= s < t < len(adj)
  translate = lambda v: v if v < t else v - 1 if v > t else s
  res = [[] for _ in range(len(adj) - 1)]
  for v, ws in enumerate(adj):
    i = translate(v)
    for w in ws:
      j = translate(w)
      if i != j:
        res[i].append(j)
  return res


def Solve(adj):
  # Solve using Stoer-Wagner. `sizes` is used to track the number of vertices
  # represented by merged vertices, which we need to calculate the answer.
  sizes = [1]*len(adj)
  while len(adj) > 1:
    s, t, min_cut = MinimumCutPhase(adj)
    if min_cut == 3:
      # Solution found!
      return (sum(sizes) - sizes[t]) * sizes[t]
    assert min_cut > 3
    if s > t: s, t = t, s
    adj = Merge(adj, s, t)
    sizes[s] += sizes[t]
    del sizes[t:t + 1]


if __name__ == '__main__':
  print(Solve(ParseInput(sys.stdin)))
