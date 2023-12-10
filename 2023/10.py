import sys

# Exits per tile type, as (dr, dc) (e.g., (-1, 0) is up/north, etc.)
exits = {
  #      NORTH     WEST      EAST      SOUTH
  '|': [(-1,  0),                     ( 1,  0)],
  '-': [          ( 0, -1), ( 0,  1)          ],
  'L': [(-1,  0),           ( 0,  1)          ],
  'J': [(-1,  0), ( 0, -1)                    ],
  '7': [          ( 0, -1),           ( 1,  0)],
  'F': [                    ( 0,  1), ( 1,  0)],
  'S': [(-1,  0), ( 0, -1), ( 0,  1), ( 1,  0)],
  '.': [],
}

# Identifies for each pair of tiles whether we cross a horizontal wall when we
# move vertically between those characters. This is used by CountInterior().
#
# For example, if we go down here:
#
#       v
#      --    yes, crossing
#      7F    no, not crossing
#      ||    no, not crossing
#      LJ    yes,crossing
#
# Alternately, this can be viewed as:
#
#      v
#     ---
#     7 F
#     | |
#     L-J
#
# which makes it more obvious when we are crossing two horizontal walls.
is_crossing = {
  '--': True,
  '-7': True,
  '-J': True,
  '..': False,
  '.F': False,
  '.L': False,
  '.|': False,
  '7.': False,
  '7F': False,
  '7L': False,
  '7|': False,
  'F-': True,
  'F7': True,
  'FJ': True,
  'J.': False,
  'JF': False,
  'JL': False,
  'J|': False,
  'L-': True,
  'L7': True,
  'LJ': True,
  '|.': False,
  '|F': False,
  '|L': False,
  '||': False,
}

# Read input
grid = [list(s.strip()) for s in sys.stdin]
H = len(grid)
W = len(grid[0])

# Returns the neighbors of a tile, taking into account the exits of the tile
# itself and its neighbors.
#
# For example, in "LJ" 'J' is a neighbor of 'L' (and 'L' is a neighbor of 'J'),
# but in "LF" 'F' is not a neighbor of 'L', because while 'L' has an exit to the
# right, 'F' does not have a matching exit to the left, so the tiles are not
# connected.
def Neighbors(r, c):
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
    for r2, c2 in Neighbors(r, c):
      if (r2, c2) not in dist:
        dist[r2,c2] = dist[r,c] + 1
        todo.append((r2, c2))

  def ReachableNeighbors(r, c):
    return [rc for rc in Neighbors(r, c) if rc in dist]

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
def CountInterior():
  return sum(
      sum(is_crossing[grid[r2][c - 1] + grid[r2][c]] for r2 in range(r)) % 2
      for r in range(1, H - 1)
      for c in range(1, W - 1)
      if grid[r][c] == '.')


answer1 = IsolateLoop()
print(answer1)

answer2 = CountInterior()
print(answer2)
