import sys

lines = sys.stdin.read().splitlines()
grid = list(list(line) for line in lines)
H = len(grid)
W = len(grid[0])


class Tumbler:
  def __init__(self, start, stride):
    self.start = start
    self.stride = stride
    self.adjacent = []
    self.count = 0

  def Process(self, todo):
    assert self.count <= len(self.adjacent)
    for t in self.adjacent[:self.count]:
      if t.count == 0:
        todo.append(t)
      t.count += 1
    self.count = 0

  def GetIndices(self):
    return range(self.start, self.start + self.stride*self.count, self.stride)

  def __repr__(self):
    return 'Tumbler(%d,%d)' % (self.start, self.stride)


def TumbleOnce(todo):
  next_todo = []
  for t in todo:
    t.Process(next_todo)
  return next_todo

def Solve(lines, part2):
  flat = sum(grid, start=[])

  directions = [
    [(c,              H,  W) for c in range(W)],  # north: columns
    [(W*r,            W, +1) for r in range(H)],  # west:  rows
    [((H - 1)*W + c,  H, -W) for c in range(W)],  # south: reverse columns
    [(W*r + W-1,      W, -1) for r in range(H)],  # east:  reverse rows
  ]

  tumblers = [[None]*(H * W) for _ in directions]

  # Create tumblers
  for direction, lines in enumerate(directions):
    for start, count, stride in lines:
      t = None
      for i in range(start, start + count*stride, stride):
        if flat[i] == '#':
          t = None
        else:
          if t is None:
            t = Tumbler(i, stride)
          tumblers[direction][i] = t

  # Connect tumblers
  for direction, lines in enumerate(directions):
    next_direction = (direction + 1) % len(directions)
    for start, count, stride in lines:
      for i in range(start, start + count*stride, stride):
        t = tumblers[direction][i]
        if t is not None:
          u = tumblers[next_direction][i]
          assert u is not None
          t.adjacent.append(u)

  # Fill initial tumblers
  todo = []
  for i, ch in enumerate(flat):
    if ch == 'O':
      t = tumblers[0][i]
      if t.count == 0:
        todo.append(t)
      t.count += 1


  # def Print(todo):
  #   coords = set([(i // W, i % W) for t in todo for i in t.GetIndices()])
  #   for i, row in enumerate(grid):
  #     print(''.join('#' if ch == '#' else '.O'[(i, j) in coords] for j, ch in enumerate(row)))


  if part2:
    for _ in directions[1:]:
      # Print(todo)
      # print()
      todo = TumbleOnce(todo)

    # Part 2 solution
    def Step(todo):
      for _ in directions:
        todo = TumbleOnce(todo)
      return todo

    def Key(todo):
      return tuple(t.count for t in todo)

    # Simulate until we find a cycle.
    seen = {}
    steps = 1
    while (key := Key(todo)) not in seen:
      # Print(todo)
      # print()
      seen[key] = steps
      todo = Step(todo)
      steps += 1


    # Finish remaining steps
    cycle_length = steps - seen[key]
    remaining_steps = 1000000000 - steps
    assert remaining_steps >= 0
    remaining_steps %= cycle_length
    for _ in range(remaining_steps):
      todo = Step(todo)

  return sum(H - (i // W) for t in todo for i in t.GetIndices())

print(Solve(lines, False))  # part 1
print(Solve(lines, True))   # part 2
