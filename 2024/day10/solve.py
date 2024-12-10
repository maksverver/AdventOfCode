import sys

grid = [
    [int(ch) for c, ch in enumerate(line.strip())]
    for r, line in enumerate(sys.stdin)]
H = len(grid)
W = len(grid[0])

def Neighbors(v):
    r, c = v
    return [(rr, cc) for (rr, cc) in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            if 0 <= rr < H and 0 <= cc < W and grid[r][c] + 1 == grid[rr][cc]]

def CountTotalPeaks(v):
    # Flood fill to find reachable peaks.
    seen = {v}
    todo = [v]
    for v in todo:
        for w in Neighbors(v):
            if w not in seen:
                seen.add(w)
                todo.append(w)
    return sum(grid[r][c] == 9 for (r, c) in seen)

def CountTotalPaths(v):
    # Depth-first search to find distinct paths.
    todo = [v]
    for v in todo:
        todo.extend(Neighbors(v))
    return sum(grid[r][c] == 9 for (r, c) in todo)

def Solve(f):
    return sum(f((r, c)) for r in range(H) for c in range(W) if grid[r][c] == 0)
   
print(Solve(CountTotalPeaks))  # Part 1
print(Solve(CountTotalPaths))  # Part 2

