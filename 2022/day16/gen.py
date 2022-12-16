#!/usr/bin/env python3

from random import *
import sys

def sattolo_cycle(items):
    """Sattolo's algorithm."""
    i = len(items)
    while i > 1:
      i = i - 1
      j = randrange(i)  # 0 <= j <= i-1
      items[j], items[i] = items[i], items[j]

min_rate = 1
max_rate = 1000
symmetric = True  # roughly doubles the size
total_graph = False

# Large 1 (larger number of edges)
#V, E, F = 50, 500, 15

# Large 2 (larger number of nodes)
#V, E, F = 150, 1000, 15

# Large 3 (asymmetric)
#V, E, F = 50, 1000, 15
#symmetric = False

# Large 4 (total graph)
#V, E, F, = 50, None, 15
#total_graph = True

# Large 5 (larger number of faucets)
#V, E, F = 50, 500, 18

# Large 6 (larger number of faucets; asymmetric)
#V, E, F = 50, 500, 21
#symmetric = False

# Large 7 (large number of faucets, but only some reachable!
#V, E, F = 400, 450, 42
#symmetric = False

# Large 8 (large number of faucets, symmetric)
#V, E, F = 50, 500, 24
#symmetric = False

# TODO: large number of faucets in an (almost) total graph so it doesn't matter
# which one you visit first?

assert total_graph or E >= V
assert F <= V

if total_graph:
  edge_counts = None
  edges = [[w for w in range(V) if v != w] for v in range(V)]
else:
  # This counts outgoing edges only
  edge_counts = [1] * V
  for i in choices(range(V), k=E - V):
    edge_counts[i] += 1

  edges = [[] for v in range(V)]
  if not symmetric:
    # Guarantee all vertices are reachable by placing them on a random cycle
    edges = [None]*V
    cycle = list(range(V))
    sattolo_cycle(cycle)
    for v, w in enumerate(cycle):
      assert v != w
      edges[v] = [w]
  for v in range(V):
    extra = edge_counts[v] - len(edges[v])
    if extra > 0:
      candidates = [u for u in range(V) if u != v and u not in edges[v]
        and (not symmetric or v not in edges[u])]
      edges[v].extend(sample(candidates, k=extra))

  if symmetric:
    edges_deep_copy = [list(adj) for adj in edges]
    for v, adj in enumerate(edges_deep_copy):
      for w in adj:
        edges[w].append(v)

for es in edges:
  shuffle(es)



flow_rates = [0] * V
for i in sample(range(V), k=F):
  flow_rates[i] = randint(min_rate, max_rate)

all_names = [chr(65 + i) + chr(65 + j) for i in range(26) for j in range(26)]
names = all_names[:1] + sample(all_names[1:], k=V - 1)
shuffle(names)

for v in range(V):
  line = 'Valve {} has flow rate={}; '.format(names[v], flow_rates[v])
  line += 'tunnel leads to valve ' if len(edges[v]) == 1 else 'tunnels lead to valves '
  line += ', '.join(names[w] for w in edges[v])
  print(line)
