import sys

shapes = [
  ['####'],

  ['.#.'
  ,'###'
  ,'.#.'],

  # Note: inverted so the bottom comes first.
  ['###'
  ,'..#'
  ,'..#'],

  ['#'
  ,'#'
  ,'#'
  ,'#'],

  ['##'
  ,'##'],
]

W = 7

directions = sys.stdin.readline().strip()

def Solve(num_to_drop, detect_cycles):
  grid = []
  time = 0
  dropped = 0
  rows_removed = 0
  seen = {} if detect_cycles else None

  def Fits(shape, x, y):
    for i, row in enumerate(shape):
      if y + i >= len(grid):
        break
      for j, ch in enumerate(row):
        if ch == '#' and grid[y + i][x + j] != '.':
          return False
    return True

  def Place(shape, x, y):
    for i, row in enumerate(shape):
      if y + i == len(grid):
        grid.append(['.']*W)
      for j, ch in enumerate(row):
        assert 0 <= x + j < W
        if ch == '#':
          assert grid[y + i][x + j] == '.'
          grid[y + i][x + j] = '#'

  def DropPiece(shape):
    nonlocal time
    x = 2
    y = len(grid) + 3
    while True:
      d = directions[time % len(directions)]
      dx = (d == '>') - (d == '<')
      time += 1
      if 0 <= x + dx <= W - len(shape[0]) and Fits(shape, x + dx, y):
        x += dx
      if y > 0 and Fits(shape, x, y - 1):
        y -= 1
      else:
        Place(shape, x, y)
        return

  def CalculateUnreachableRows():
    # Check how many rows we can remove from the bottom of the grid because
    # the cells are no not reachable from the top.
    #
    # Note that we need to check left, right and below only (not above),
    # since blocks cannot move up. See the examples below (+ is reachable,
    # . is unreachable):
    #
    #    +++###+    ++####+
    #    +#####+    +#####+
    #    ##...#+    ##...#+
    #    ##+++++    ##.#+++
    #
    # A dumber way is to just remove everything beneath e.g. row 1000 but
    # that's using an unproven assumption.
    #return max(0, len(grid) - 1000) # dumb version
    reachable = [True]*W
    for y in reversed(range(len(grid))):
      reachable = [r and ch == '.' for r, ch in zip(reachable, grid[y])]
      for x in range(1, W):
        if reachable[x - 1] and not reachable[x] and grid[y][x] == '.':
          reachable[x] = True
        if reachable[W - x] and not reachable[W - x - 1] and grid[y][W - x - 1] == '.':
          reachable[W - x - 1] = True
      if not any(reachable):
        return y + 1
    return 0

  def CullGrid():
    nonlocal grid, rows_removed
    n = CalculateUnreachableRows()
    if n > 0:
      del grid[:n]
      rows_removed += n
    return n

  def DetectCycles():
    nonlocal dropped, rows_removed, detect_cycles
    key = ''.join(''.join(row) for row in grid), dropped % len(shapes), time % len(directions)
    if key in seen:
      prev_dropped, prev_rows_removed = seen[key]
      cycle_length = dropped - prev_dropped
      cycle_count = (num_to_drop - dropped) // cycle_length
      rows_removed += cycle_count * (rows_removed - prev_rows_removed)
      dropped += cycle_count * cycle_length
      # No point in detecting more cycles which will all have the same length
      detect_cycles = False
    else:
      seen[key] = dropped, rows_removed

  # Finally, the actual top-level algorithm!
  while dropped < num_to_drop:
    DropPiece(shapes[dropped % len(shapes)])
    dropped += 1
    if CullGrid() and detect_cycles:
      DetectCycles()

  return len(grid) + rows_removed

print(Solve(2022, False))
print(Solve(10**12, True))
