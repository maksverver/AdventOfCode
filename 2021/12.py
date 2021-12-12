from collections import defaultdict
import sys

adj = defaultdict(set)
for line in sys.stdin:
    v, w = line.strip().split('-')
    adj[v].add(w)
    adj[w].add(v)

def Solve(allow_extra_visit):
    paths = 0
    visited = defaultdict(int)

    def Dfs(v, allow_extra_visit):
        if v == 'end':
            nonlocal paths
            paths += 1
        visited[v] += 1
        for w in adj[v]:
            use_extra_visit = (allow_extra_visit and w.islower() and
                    visited[w] == 1 and w not in ('start', 'end'))
            if use_extra_visit or w.isupper() or visited[w] == 0:
                Dfs(w, allow_extra_visit and not use_extra_visit)
        visited[v] -= 1

    Dfs('start', allow_extra_visit)
    return paths

print(Solve(False))  # part 1
print(Solve(True))   # part 2
