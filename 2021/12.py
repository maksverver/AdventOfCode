from collections import defaultdict
import sys

adj = defaultdict(set)
for line in sys.stdin:
    v, w = line.strip().split('-')
    adj[v].add(w)
    adj[w].add(v)

def Solve(allow_extra_visit):
    paths = 0
    visited = set(['start'])

    def Dfs(v):
        nonlocal allow_extra_visit, paths
        if v == 'end':
            paths += 1
            return
        for w in adj[v]:
            if w.isupper():
                # Large cave, can be visited multiple times
                Dfs(w)
            elif w not in visited:
                # Small cave, not visited before
                visited.add(w)
                Dfs(w)
                visited.remove(w)
            elif allow_extra_visit and w != 'start':
                # Small cave, one extra visit allowed
                allow_extra_visit = False
                Dfs(w)
                allow_extra_visit = True

    Dfs('start')
    return paths

print(Solve(False))  # part 1
print(Solve(True))   # part 2
