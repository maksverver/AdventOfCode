import re
import sys

grid = [['.' for _ in range(50)] for _ in range(6)]

def FillRect(w, h):
  for r in range(h):
    for c in range(w):
      grid[r][c] = '#'

def RotateRow(y, n):
  global grid
  grid[y] = grid[y][-n:] + grid[y][:-n]

def RotateCol(x, n):
  global grid
  grid = list(map(list, zip(*grid)))
  RotateRow(x, n)
  grid = list(map(list, zip(*grid)))

def PrintCount():
  print(sum(cell == '#' for row in grid for cell in row))

def PrintGrid():
  for row in grid:
    print(''.join(row))

FillRect.pattern = 'rect ([0-9]+)x([0-9]+)'
RotateRow.pattern = 'rotate row y=([0-9]+) by ([0-9]+)'
RotateCol.pattern = 'rotate column x=([0-9]+) by ([0-9]+)'
for line in sys.stdin:
  for func in (FillRect, RotateRow, RotateCol):
    m = re.match(func.pattern, line)
    if m:
      func(*map(int, m.groups()))
      break
  else:
    sys.stderr.write('Error! Unrecognized command line: ' + line)
PrintCount()
PrintGrid()
