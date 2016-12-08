import numpy as np
import re
import sys

grid = np.zeros((6, 50), dtype=np.bool)

def FillRect(w, h):
  grid[:h,:w] = 1

def RotateRow(y, n):
  grid[y] = np.roll(grid[y], n)

def RotateCol(x, n):
  grid[:,x] = np.roll(grid[:,x], n)

def PrintCount():
  print np.count_nonzero(grid)

def PrintGrid():
  for row in grid:
    print ''.join(".#"[cell] for cell in row)

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
