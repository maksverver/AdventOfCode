from collections import defaultdict
import sys

# adj[v] is the set of vertices w connected to v
adj = defaultdict(set)
for line in sys.stdin:
    v, w = line.strip().split('-')
    assert v != w  # assume we have no loops
    adj[v].add(w)
    adj[w].add(v)


# Part 1: find all ordered vertex triples (u, v, w) so that they are all connected
# and at least one of them has a name that starts with 't':

print(sum(
        u.startswith('t') or v.startswith('t') or w.startswith('t')
        for u in adj
        for v in adj[u] if u < v
        for w in adj[u] & adj[v] if v < w))


# Part 2: find the largest clique.
#
# Apparently the Bron-Kerbosh algorithm is a relatively efficient way to
# enumerate all maximal cliques in a graph:
# https://en.wikipedia.org/wiki/Bron-Kerbosch_algorithm

def BronKerbosch1(R, P, X):
    if not P and not X:
        yield R

    for v in P:
        yield from BronKerbosch1(R | {v}, P & adj[v], X & adj[v])
        P = P - {v}
        X = X | {v}


def BronKerbosch2(R, P, X):
    if not P and not X:
        yield R

    u = next(iter(P))
    for v in P - adj[u]:
        yield from BronKerbosch1(R | {v}, P & adj[v], X & adj[v])
        P = P - {v}
        X = X | {v}


lengths = list(map(len, BronKerbosch2(set(), set(adj), set())))
assert lengths.count(max(lengths)) == 1

max_clique = max(BronKerbosch2(set(), set(adj), set()), key=len)
print(','.join(sorted(max_clique)))

assert max_clique == max(BronKerbosch1(set(), set(adj), set()), key=len)
