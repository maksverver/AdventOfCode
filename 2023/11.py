from itertools import accumulate
import sys

# Read input
grid = [s.strip() for s in sys.stdin]
H = len(grid)
W = len(grid[0])

# Find initial location of galaxies
galaxies = [(r, c) for r in range(H) for c in range(W) if grid[r][c] == '#']
N = len(galaxies)


def Solve(expand):
  # Calculate new coordinates for rows and columns:
  def RowSize(i): return expand if all(grid[i][j] == '.' for j in range(W)) else 1
  def ColSize(j): return expand if all(grid[i][j] == '.' for i in range(H)) else 1
  new_r = list(accumulate(RowSize(i) for i in range(H)))
  new_c = list(accumulate(ColSize(j) for j in range(W)))

  # Calculate sum of pairwise Manhattan distances of new coordinates:
  def Dist(i, j):
    r1, c1 = galaxies[i]
    r2, c2 = galaxies[j]
    return abs(new_r[r1] - new_r[r2]) + abs(new_c[c1] - new_c[c2])
  return sum(Dist(i, j) for i in range(N) for j in range(i + 1, N))


# Part 1
print(Solve(2))

# Part 2
print(Solve(1000000))
