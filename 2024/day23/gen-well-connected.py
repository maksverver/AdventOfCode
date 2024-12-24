# Intended to break non-backtracking solutions.
#
# There are two cliques, one slightly larger than the other.
#
# Every vertex in the small clique is also connected to every vertex in the large clique
# except for two. The edges between small and large clique must be chosen so that no two
# small vertices exclude the same two large vertices.
#
# challenge-6.txt: python3 gen-well-connected.py 25
# challenge-7.txt: python3 gen-well-connected.py 100
# challenge-8.txt: python3 gen-well-connected.py 338

from collections import defaultdict
from random import shuffle
import sys

def shuffled(iterable):
    l = list(iterable)
    shuffle(l)
    return l

# Size of large clique
N, = map(int, sys.argv[1:])
assert 1 < N <= 338

small_clique = range(0, N - 1)
large_clique = range(N - 1, N - 1 + N)

edges = []
for v in small_clique:
    for w in small_clique:
        if v < w:
            edges.append((v, w))
for v in large_clique:
    for w in large_clique:
        if v < w:
            edges.append((v, w))
for v in small_clique:
    for w in list(large_clique)[:v] + list(large_clique)[v+2:]:
        assert v < w
        edges.append((v, w))

assert len(edges) == len(set(edges))

names = shuffled(chr(ord('a') + i) + chr(ord('a') + j) for i in range(26) for j in range(26))

adj = defaultdict(set)
for v, w in edges:
    adj[v].add(w)
    adj[w].add(v)

# Answer to part 1
print(sum(
        names[u].startswith('t') or names[v].startswith('t') or names[w].startswith('t')
        for u in adj
        for v in adj[u] if u < v
        for w in adj[u] & adj[v] if v < w),
    file=sys.stderr)

# Answer to part 2
for e in shuffled(edges):
    print('-'.join(names[v] for v in shuffled(e)))
print(','.join(sorted(names[v] for v in large_clique)), file=sys.stderr)
