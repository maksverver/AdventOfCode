import sys

# Read input grid.
grid = {(r, c): ch
        for r, line in enumerate(sys.stdin)
        for c, ch in enumerate(line.strip())}

# Find start and end location.
start, = (v for v, ch in grid.items() if ch == 'S')
end,   = (v for v, ch in grid.items() if ch == 'E')

def Neighbors(v):
    r, c = v
    return [(r-1, c), (r, c-1), (r, c+1), (r+1, c)]

# Breadth-first search to find all distances of cells reachable from `start`.
def FindDistances(start):
    dists = {start: 0}
    todo = [start]
    for v in todo:
        for w in Neighbors(v):
            if grid.get(w, '#') != '#' and w not in dists:
                dists[w] = dists[v] + 1
                todo.append(w)
    return dists

# Find distances from start and to end.
dists1 = FindDistances(start)
dists2 = FindDistances(end)
min_dist = min(d + dists2[v] for v, d in dists1.items())
max_dist = max(d + dists2[v] for v, d in dists1.items())
# My solution doesn't require this, but apparently the input is a labyrinth,
# i.e. one connected path without branches.
assert min_dist == max_dist

def Solve(max_shortcut, min_saved=100):
    answer = 0
    for v in dists1:
        r, c = v
        for dr in range(-max_shortcut, max_shortcut + 1):
            for dc in range(-max_shortcut + abs(dr), max_shortcut - abs(dr) + 1):
                w = (r + dr, c + dc)
                if w in dists2:
                    new_dist = dists1[v] + dists2[w] + abs(dr) + abs(dc)
                    if min_dist - new_dist >= min_saved:
                        answer += 1
    return answer

for max_shortcut in 2, 20:
    print(Solve(max_shortcut))
