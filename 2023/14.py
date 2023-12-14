import sys

def Solve(lines, part2):
  grid = list(list(line) for line in lines)
  H = len(grid)
  W = len(grid[0])

  directions = [
    [[(r, c) for r in range(H)]           for c in range(W)],  # north: columns
    [[(r, c) for c in range(W)]           for r in range(H)],  # west:  rows
    [[(r, c) for r in reversed(range(H))] for c in range(W)],  # south: reverse columns
    [[(r, c) for c in reversed(range(W))] for r in range(H)],  # east:  reverse rows
  ]

  # Moves all boulders towards the front in a single line. For example,'.O.O#O.O'
  # becomes 'OO..#OO.'. The line is given as a list of coordinates in the 2D grid,
  # so the same function can be used in all directions.
  #
  # For example, if line=[(0, 0), (0, 1), (0, 2)...] then the top row of the grid
  # will be tumbled to the left (west).
  def TumbleLine(line):
    def Get(i):
      r, c = line[i]
      return grid[r][c]

    def Set(i, v):
      r, c = line[i]
      grid[r][c] = v

    i = 0  # next place where a boulder will fall
    for j in range(len(line)):
      ch = Get(j)
      if ch == '#':
        i = j + 1
      elif ch == 'O':
        if i < j:
          Set(j, '.')
          Set(i, 'O')
        i = i + 1

  def Tumble(lines):
    for line in lines:
      TumbleLine(line)

  if not part2:
    # Part 1 solution
    Tumble(directions[0])  # north

  else:
    # Part 2 solution
    def Step():
      for lines in directions:
        Tumble(lines)

    # Simulate until we find a cycle.
    seen = {}
    steps = 0
    while (key := ''.join(''.join(row) for row in grid)) not in seen:
      seen[key] = steps
      Step()
      steps += 1

    # Finish remaining steps
    cycle_length = steps - seen[key]
    remaining_steps = 1000000000 - steps
    assert remaining_steps >= 0
    remaining_steps %= cycle_length
    for _ in range(remaining_steps):
      Step()

  return sum(H - i for i, row in enumerate(grid) for ch in row if ch == 'O')


lines = sys.stdin.read().splitlines()
print(Solve(lines, False))  # part 1
print(Solve(lines, True))   # part 2
