from math import inf
import sys

# Read input grid.
grid = [list(line.strip()) for line in sys.stdin]
H = len(grid)
W = len(grid[0])

# Find start and end location.
start, = ((r, c) for r in range(H) for c in range(W) if grid[r][c] == 'S')
end,   = ((r, c) for r in range(H) for c in range(W) if grid[r][c] == 'E')

def Neighbors(r, c):
    return [(r-1, c), (r, c-1), (r, c+1), (r+1, c)]

# Breadth-first search to find all distances of cells reachable from `start`.
def FindDistances(start):
    dists = [[inf]*W for _ in range(H)]
    todo = [start]
    dists[start[0]][start[1]] = 0
    for r1, c1 in todo:
        for r2, c2 in Neighbors(r1, c1):
            if grid[r2][c2] != '#' and dists[r2][c2] == inf:
                dists[r2][c2] = dists[r1][c1] + 1
                todo.append((r2, c2))
    return dists

# Find distances from start and to end.
dists1 = FindDistances(start)
dists2 = FindDistances(end)
min_dist = dists1[end[0]][end[1]]

def Solve(max_shortcut, min_saved=100):
    answer = 0
    for r in range(H):
        for c in range(W):
            if dists1[r][c] < inf:
                for dr in range(-max_shortcut, max_shortcut + 1):
                    for dc in range(-max_shortcut + abs(dr), max_shortcut - abs(dr) + 1):
                        r2 = r + dr
                        c2 = c + dc
                        if 0 <= r2 < H and 0 <= c2 < W and dists2[r2][c2] < inf:
                            new_dist = dists1[r][c] + dists2[r2][c2] + abs(dr) + abs(dc)
                            if min_dist - new_dist >= min_saved:
                                #print(min_dist - new_dist)
                                answer += 1
    return answer

for max_shortcut in 2, 20:
    print(Solve(max_shortcut))
