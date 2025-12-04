import sys

index    = {}
edges    = []
degree   = []

v = 0
for r, line in enumerate(sys.stdin):
    for c, ch in enumerate(line):
        if ch == '@':
            index[r, c] = v
            edges.append([])
            degree.append(0)
            for neighbor in [(r-1, c-1), (r-1,  c), (r-1,  c+1), (r, c-1)]:
                w = index.get(neighbor, -1)
                if w >= 0:
                    degree[v] += 1
                    degree[w] += 1
                    edges[v].append(w)
                    edges[w].append(v)
            v += 1

todo = [v for v, d in enumerate(degree) if d < 4]
print(len(todo))  # Part 1
for v in todo:
    for w in edges[v]:
        if degree[w] == 4:
            todo.append(w)
        degree[w] -= 1
print(len(todo))  # Part 2
