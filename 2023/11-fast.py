# Advent of Code 2013 Dag 11 -- O(N) solution
# https://adventofcode.com/2023/day/11
#
# See also:
#
#   - day11/snel-met-uitleg.py for an explanation (in Dutch).
#
#   - day11/fast.py for a slightly different fast solution that combines
#     translating coordinates with summing distances.
#
#   - day11/fast-numpy.py: for the fastest version which uses numpy to speed up
#     parsing.
#

from itertools import accumulate
import sys

# Stap 0: read input
grid = [s.strip() for s in sys.stdin]
H = len(grid)     # height
W = len(grid[0])  # width

for expand in (2, 1_000_000):

  # Step 1: translate coordinates
  x_sizes = [expand if all(grid[y][x] == '.' for y in range(H)) else 1 for x in range(W)]
  y_sizes = [expand if all(grid[y][x] == '.' for x in range(W)) else 1 for y in range(H)]
  new_x = list(accumulate(x_sizes, initial=0))
  new_y = list(accumulate(y_sizes, initial=0))
  xs = [new_x[x] for x in range(W) for y in range(H) if grid[y][x] == '#']
  ys = [new_y[y] for y in range(H) for x in range(W) if grid[y][x] == '#']

  # Step 2: calculate sum of distances for x- and y-coordinates seaparately.
  # Requires that `xs` and `ys` are sorted!
  print(
    sum((xs[i] - xs[i - 1]) * i * (len(xs) - i) for i in range(1, len(xs))) +
    sum((ys[i] - ys[i - 1]) * i * (len(ys) - i) for i in range(1, len(ys))))
