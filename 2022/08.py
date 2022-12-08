import sys

grid = [list(map(int, line.strip())) for line in sys.stdin]

H = len(grid)
W = len(grid[0])

# A list of list of coordinates representing all the orthogonal lines through
# the grid: rows, columns, reverse rows, reverse columns.
lines = (
  [[(r, c) for c in range(W)] for r in range(H)] +
  [[(r, c) for r in range(H)] for c in range(W)] +
  [[(r, c) for c in reversed(range(W))] for r in range(H)] +
  [[(r, c) for r in reversed(range(H))] for c in range(W)]
)

def SolvePart1():
  visible = [[False for _ in row] for row in grid]
  for line in lines:
    last_height = -1
    for r, c in line:
      h = grid[r][c]
      if h > last_height:
        last_height = h
        visible[r][c] = True
  return sum(map(sum, visible))

def SolvePart2():
  scores = [[1 for _ in row] for row in grid]
  for height in range(10):
    for line in lines:
      n = 0
      for r, c in line:
        h = grid[r][c]
        if h == height:
          scores[r][c] *= n
        if h < height:
          n += 1
        else:
          n = 1
  return max(map(max, scores))

print(SolvePart1())
print(SolvePart2())
