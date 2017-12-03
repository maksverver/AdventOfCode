import sys

N = int(sys.stdin.readline())

grid = {(0, 0): 1}
x, y = 0, 0
dx, dy = 1, 0
while grid[x, y] <= N:
  x += dx
  y += dy
  grid[x, y] = sum(
      grid.get((nx, ny), 0)
      for nx in (x - 1, x, x + 1)
      for ny in (y - 1, y, y + 1))
  ndx, ndy = -dy, dx
  if (x + ndx, y + ndy) not in grid:
    dx, dy = ndx, ndy
print(grid[x, y])
