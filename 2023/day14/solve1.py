import sys

lines = sys.stdin.read().splitlines()
grid = list(list(line) for line in lines)
H = len(grid)
W = len(grid[0])

def Solve(lines, part2):
  flat = sum(grid, start=[])

  directions = [
    [(c,              H,  W) for c in range(W)],  # north: columns
    [(W*r,            W, +1) for r in range(H)],  # west:  rows
    [((H - 1)*W + c,  H, -W) for c in range(W)],  # south: reverse columns
    [(W*r + W-1,      W, -1) for r in range(H)],  # east:  reverse rows
  ]

  def TumbleLine(start, count, stride):
    i = start  # next place where a boulder will fall
    for j in range(start, start + count*stride, stride):
      if (ch := flat[j]) == '#':
        i = j + stride
      elif ch == 'O':
        if i != j:
          flat[j] = '.'
          flat[i] = 'O'
        i += stride

  def Tumble(lines):
    for start, count, stride in lines:
      TumbleLine(start, count, stride)

  if not part2:
    # Part 1 solution
    Tumble(directions[0])  # north
    # for i in range(H):
    #   print(''.join(flat[i*W:(i+1)*W]))

  else:
    # Part 2 solution
    def Step():
      for lines in directions:
        Tumble(lines)

    # Simulate until we find a cycle.
    seen = {}
    steps = 0
    while (key := ''.join(flat)) not in seen:
      seen[key] = steps
      Step()
      steps += 1

    # Finish remaining steps
    cycle_length = steps - seen[key]
    print(cycle_length)
    remaining_steps = 1000000000 - steps
    assert remaining_steps >= 0
    remaining_steps %= cycle_length
    for _ in range(remaining_steps):
      Step()

  return sum(H - (i // W) for i, ch in enumerate(flat) if ch == 'O')


print(Solve(lines, False))  # part 1
print(Solve(lines, True))   # part 2
