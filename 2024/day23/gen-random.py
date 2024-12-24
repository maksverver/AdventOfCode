from random import choice, sample, shuffle
from collections import defaultdict
import sys

def shuffled(iterable):
    l = list(iterable)
    shuffle(l)
    return l

adj = defaultdict(set)

# Note: there can be at most 676 vertices (because of "xx" naming scheme)
# so each vertex can have at most 675 neighbors.

# Challenge case parameters:
#
# challenge-1.txt: 10 19 40
# challenge-2.txt: 12 24 50
# challenge-3.txt: 15 29 60
# challenge-4.txt: 20 35 100    (440 vertices)
# challenge-5.txt: 35 49 300    (630 vertices)

clique_size_min, clique_size_max, max_neighbors = map(int, sys.argv[1:])
assert 0 < clique_size_min <= clique_size_max <= max_neighbors
clique_sizes = range(clique_size_min, clique_size_max + 1)
assert sum(clique_sizes) < 26**2

cliques = []
clique_id = []
V = 0
for i, clique_size in enumerate(clique_sizes):
    clique = range(V, V + clique_size)
    cliques.append(clique)
    for v in clique:
        for w in clique:
            if v != w:
                adj[v].add(w)
    clique_id += [i] * clique_size
    V += clique_size

edges = set((v, w) for v in range(V) for w in range(v + 1, V))

# Super brute force way to ensure maximum clique is well defined: for each vertex v,
# remove edge to TWO random vertices in each other clique (removing one vertex
# would ensure that the clique is maximal, but could introduce duplicates; removing
# two guarantees the largest clique is unique, though smaller cliques might not be).
#
# Note: this is not be 100% correct. We should ensure that any two vertices in a
# smaller clique do not omit the same to edges from the larger clique, otherwise
# those two verteces from the smaller clique could substitute for the two
# vertices in the larger clique being avoided. But the current code doesn't do
# that and relies just on chance.
#
# See gen-well-connected.py for a more principled approach.
for i in range(len(cliques)):
    for j in range(len(cliques)):
        if i != j:
            for v in cliques[i]:
                remaining = [w for w in cliques[j] if (min(v, w), max(v, w)) in edges]
                for w in sample(remaining, k=min(2, len(remaining))):
                    edges.remove((min(v, w), max(v, w)))

# Now add a bunch of random edges between different cliques:
for v, w in shuffled(edges):
    if len(adj[v]) < max_neighbors and len(adj[w]) < max_neighbors and v not in adj[w]:
        adj[v].add(w)
        adj[w].add(v)

assert len(adj) == sum(clique_sizes)

#print(*map(len, adj.values()))

names = shuffled(chr(ord('a') + i) + chr(ord('a') + j) for i in range(26) for j in range(26))
edges = shuffled(shuffled([names[v], names[w]]) for v in adj for w in adj[v] if v < w)
for v, w in edges:
    print(v, w, sep='-')

# Answer to part 1
print(sum(
        names[u].startswith('t') or names[v].startswith('t') or names[w].startswith('t')
        for u in adj
        for v in adj[u] if u < v
        for w in adj[u] & adj[v] if v < w),
    file=sys.stderr)

# Answer to part 2
print(','.join(sorted(names[v] for v in range(V - clique_size, V))), file=sys.stderr)
