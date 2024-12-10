import sys

grid = {(r, c): int(ch) for r, line in enumerate(sys.stdin) for c, ch in enumerate(line.strip())}

def Neighbors(v):
    r, c = v
    return [w for w in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            if w in grid and grid[v] + 1 == grid[w]]

def CountTotalPeaks(v):
    seen = {v}
    todo = [v]
    for v in todo:
        for w in Neighbors(v):
            if w not in seen:
                seen.add(w)
                todo.append(w)
    return sum(grid[v] == 9 for v in seen)

def CountTotalPaths(v):
    return 1 if grid[v] == 9 else sum(CountTotalPaths(w) for w in Neighbors(v))

def Solve(f):
    return sum(f(p) for p, v in grid.items() if v == 0)
   
print(Solve(CountTotalPeaks))  # Part 1
print(Solve(CountTotalPaths))  # Part 2

