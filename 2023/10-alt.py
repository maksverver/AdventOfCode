import sys

NORTH = ( -1,  0)
EAST  = (  0, +1)
SOUTH = ( +1,  0)
WEST  = (  0, -1)

exits = {
  '|': [NORTH, SOUTH],
  '-': [EAST, WEST],
  'L': [NORTH, EAST],
  'J': [NORTH, WEST],
  '7': [SOUTH, WEST],
  'F': [SOUTH, EAST],
  'S': [NORTH, EAST, SOUTH, WEST],
  '.': [],
}

# Read input
grid = [list(s.strip()) for s in sys.stdin]
H = len(grid)
W = len(grid[0])

# Returns a coordinates of tiles connected to the tile at (r,c).
#
# Not all tiles that are adjacent are connected; their exits must match too.
# For example, in "LJ", 'L' and 'J' are connected, but in "LF", 'L' and 'F' are
# not connected, because while 'L' has an exit to the right, 'F' does not have a
# matching exit to the left.
def Connections(r, c):
  res = []
  for dr, dc in exits[grid[r][c]]:
    r2, c2 = r + dr, c + dc
    if 0 <= r2 < H and 0 <= c2 < W and (-dr, -dc) in exits[grid[r2][c2]]:
      res.append((r2, c2))
  return res


# Detects the loop, assuming that tiles in the loop are only connected to
# each other, and nothing else!
def IsolateLoop():
  v0, = ((r, c) for r in range(H) for c in range(W) if grid[r][c] == 'S')
  v1, v2 = Connections(*v0)
  loop = [v0, v1]
  while loop[-1] != v2:
    v, = (v for v in Connections(*loop[-1]) if v != loop[-2])
    loop.append(v)
  return loop


# Create a new grid of double size:
#
#   12345
# 1 ..F7.
# 2 .FJ|.
# 3 SJ.L7
# 4 |F--J
# 5 LJ...
#
# Becomes:
#
# ...........
# .....F-7...
# .....|.|...
# ...F-J.|...
# ...|...|...
# .S-J...L-7.
# .|.......|.
# .|.F-----J.
# .|.|.......
# .L.J.......
# ...........

def ExpandGrid():
  global H2, W2, grid2
  W2 = 2*W + 1
  H2 = 2*H + 1
  grid2 = [['.']*W2 for _ in range(H2)]

  # Put in tiles from original grid
  for (r, c) in loop:
    grid2[2*r + 1][2*c + 1] = grid[r][c]

  # Horizontal connections
  for r in range(1, H2, 2):
    for c in range(2, W2, 2):
      if (0, 1) in exits[grid2[r][c - 1]] and (0, -1) in exits[grid2[r][c + 1]]:
        grid2[r][c] = '-'

  # Vertical connections
  for r in range(2, H2, 2):
    for c in range(1, W2, 2):
      if (1, 0) in exits[grid2[r - 1][c]] and (-1, 0) in exits[grid2[r + 1][c]]:
        grid2[r][c] = '|'


def FindInterior():
  # Flood fill starting from the top-left corner
  assert grid2[0][0] == '.'
  grid2[0][0] = 'o'
  todo = [(0, 0)]
  i = 0
  while i < len(todo):
    r, c = todo[i]
    i += 1
    for (r2, c2) in ((r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)):
      if 0 <= r2 < H2 and 0 <= c2 < W2 and grid2[r2][c2] == '.':
        grid2[r2][c2] = 'o'
        todo.append((r2, c2))

  # Count points in the original grid that are not reachable from the outside
  return sum(grid2[2*r + 1][2*c + 1] == '.' for r in range(H) for c in range(W))


# Part 1: loop length
loop = IsolateLoop()
assert len(loop) % 2 == 0
print(len(loop) // 2)

# Part 2: count interior
ExpandGrid()
answer2 = FindInterior()
print(answer2)
