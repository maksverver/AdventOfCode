import sys

grid = [s.strip() for s in sys.stdin]
H = len(grid)
W = len(grid[0])

galaxies = [(r, c) for r in range(H) for c in range(W) if grid[r][c] == '#']
N = len(galaxies)

def SolveAxis(counts):
  total_dist = 0
  acc_dist   = 0
  acc_count  = 0
  for n in counts:
    acc_dist   += acc_count*(1 + expand*(n == 0))
    acc_count  += n
    total_dist += acc_dist*n
  return total_dist

row_counts = [sum(grid[i][j] == '#' for j in range(W)) for i in range(H)]
col_counts = [sum(grid[i][j] == '#' for i in range(H)) for j in range(W)]
for expand in 1, 999999:
  print(SolveAxis(row_counts) + SolveAxis(col_counts))
