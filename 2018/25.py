import sys

def Dist(v, w):
    return sum(abs(x - y) for (x, y) in zip(v, w))

def Find(v):
    r = roots[v]
    if r != v:
        roots[v] = r = Find(roots[v])
    return r

def Union(v, w):
    v = Find(v)
    w = Find(w)
    if v == w:
        return v
    if sizes[v] < sizes[w]:
        v, w = w, v
    sizes[v] += sizes[w]
    roots[w] = roots[v]
    return v

points = [tuple(map(int, line.split(','))) for line in sys.stdin]
roots = list(range(len(points)))
sizes = [1]*len(points)
for i, p in enumerate(points):
    for j, q in enumerate(points[:i]):
        if Dist(p, q) <= 3:
            Union(i, j)

print(sum(v == roots[v] for v in range(len(points))))
