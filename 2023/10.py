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


# Detects the loop, and returns the maximum distance in the loop (which is
# simply half the loop length).
#
# Also transformats the input a bit which is helpful for part 2:
#
#  - Replaces the start symbol ('S') with an appropriate tile ('-', 'F', etc.)
#  - Replaces all tiles that are not part of the loop with ('-')
#
def IsolateLoop():

  # Identify starting point
  (r0, c0), = ((r, c) for r in range(H) for c in range(W) if grid[r][c] == 'S')

  # Step 1: a breadth-first search to identify tiles reachable from the start
  dist = {(r0, c0):0}
  todo = [(r0, c0)]
  i = 0
  while i < len(todo):
    r, c = todo[i]
    i += 1
    for r2, c2 in Connections(r, c):
      if (r2, c2) not in dist:
        dist[r2,c2] = dist[r,c] + 1
        todo.append((r2, c2))

  def ReachableNeighbors(r, c):
    return [rc for rc in Connections(r, c) if rc in dist]

  # Step 2: prune dead ends (we assume the input contains only 1 cycle
  # that is reachable from the start).
  todo = [(r, c) for (r, c) in dist if len(ReachableNeighbors(r, c)) < 2]
  for (r, c) in todo:
    del dist[r, c]
  i = 0
  while i < len(todo):
    r, c = todo[i]
    i += 1
    for r2, c2 in ReachableNeighbors(r, c):
      if len(ReachableNeighbors(r2, c2)) < 2:
        del dist[r2, r2]
        todo.append(r2, c2)

  # For Part 2: Replace letter 'S'. There should be only 1 option.
  start_dirs = sorted((r2 - r0, c2 - c0) for (r2, c2) in ReachableNeighbors(r0, c0))
  start_ch, = (ch for ch, dirs in exits.items() if sorted(dirs) == start_dirs)
  grid[r0][c0] = start_ch

  # For Part 2: Set all tiles that are not part of the loop to '.'
  for r in range(H):
    for c in range(W):
      if (r, c) not in dist:
        grid[r][c] = '.'

  # At this point, the grid only contains characters that are part of the loop,
  # so we don't need `dist` any more. The loop should have even length, and
  # therefore, the farthest point is simply halfway through the loop.
  max_dist = max(dist.values())
  assert len(dist) == max_dist * 2
  return max_dist


# Counts the number of cells that are inside the loop.
#
# This uses the principle that if we draw a line from an empty cell to outside
# the grid, then the number of walls we cross is odd iff. the cell is inside
# the loop.
#
# For example, if we go up here:
#
#      --    yes, crossing
#      7F    no, not crossing (squeeze through)
#      ||    no, not crossing (squeeze through)
#      LJ    yes,crossing
#       ^
def CountInterior():
  return sum(
      sum((r2, c) in Connections(r2, c - 1) for r2 in range(r)) % 2
      for r in range(1, H - 1)
      for c in range(1, W - 1)
      if grid[r][c] == '.')


answer1 = IsolateLoop()
print(answer1)

answer2 = CountInterior()
print(answer2)


# Alternative: walk through the grid diagonally, only counting
#  '|', '-', 'F' and 'J' as walls, but not 'L' or '7'.
def CountInterior2():
  return sum(
    sum(grid[r - i][c - i] in '|-FJ' for i in range(1, min(r, c) + 1)) % 2
    for r in range(1, H - 1) for c in range(1, W - 1) if grid[r][c] == '.')

assert answer2 == CountInterior2()
