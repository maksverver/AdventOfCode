import re
import sys

grid, directions = sys.stdin.read().split('\n\n')
grid = grid.split('\n')

H = len(grid)
W = max(len(row) for row in grid)
for r in range(H):
  grid[r] += ' '*(W - len(grid[r]))
  assert len(grid[r]) == W


DR = [0, 1,  0, -1]
DC = [1, 0, -1,  0]

r = 0
c = grid[0].index('.')
d = 0

assert re.match('^[LR0-9]*$', directions)
for direction in re.findall('[LR]|[0-9]+', directions):
  if direction == 'L':
    d = (d - 1) % 4
  elif direction == 'R':
    d = (d + 1) % 4
  else:
    for _ in range(int(direction)):
      r2 = (r + DR[d]) % H
      c2 = (c + DC[d]) % W

      while grid[r2][c2] == ' ':
        r2 = (r2 + DR[d]) % H
        c2 = (c2 + DC[d]) % W

      if grid[r2][c2] == '#':
        break
      assert grid[r2][c2] == '.'
      r, c = r2, c2

print(1000*(r + 1) + 4*(c + 1) + d)
