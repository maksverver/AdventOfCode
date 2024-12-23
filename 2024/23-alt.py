# Alternate solution that uses adjacency lists where adj[v] only
# contains adjacent vertices w > v (rather than all adjacent vertices)
#
# This simplifies some of the algorithms and makes a simple DFS sufficient
# for part 2 (which essentially constructs the clique with vertices listed
# in ascending order).
import sys

# adj[v] is the set of vertices w > v that are connected to v
adj = {}
for line in sys.stdin:
    v, w = line.strip().split('-')
    if v not in adj: adj[v] = set()
    if w not in adj: adj[w] = set()
    if v < w: adj[v].add(w)
    if v > w: adj[w].add(v)


# Part 1: find all ordered vertex triples (u, v, w) so that they are all connected
# and at least one of them has a name that starts with 't':

print(sum(
        u.startswith('t') or v.startswith('t') or w.startswith('t')
        for u in adj
        for v in adj[u]
        for w in adj[v] & adj[u]))

# Part 2: find the largest clique.
#
# We use a depth-first search to construct all cliques in vertex order.
def FindMaximumClique():
    c = []
    r = []

    def Dfs(n):
        nonlocal c, r
        if len(c) > len(r):
            r = list(c)

        for v in n:
            c.append(v)
            Dfs(n & adj[v])
            c.pop()

    for v, n in adj.items():
        c.append(v)
        Dfs(n)
        c.pop()
    return r


print(','.join(sorted(FindMaximumClique())))
