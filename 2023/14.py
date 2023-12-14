import sys

def Solve(lines, part2):
  a = list(list(line) for line in lines)
  H = len(a)
  W = len(a[0])

  def North():
    for i in range(H):
      for j in range(W):
        if a[i][j] == '.':
          k = i + 1
          while k < H and a[k][j] == '.':
            k += 1
          if k < H and a[k][j] == 'O':
            a[i][j], a[k][j] = a[k][j], a[i][j]

  def South():
    for i in reversed(range(H)):
      for j in range(W):
        if a[i][j] == '.':
          k = i - 1
          while k >= 0 and a[k][j] == '.':
            k -= 1
          if k >= 0 and a[k][j] == 'O':
            a[i][j], a[k][j] = a[k][j], a[i][j]

  def West():
    for i in range(H):
      for j in range(W):
        if a[i][j] == '.':
          k = j + 1
          while k < H and a[i][k] == '.':
            k += 1
          if k < H and a[i][k] == 'O':
            a[i][j], a[i][k] = a[i][k], a[i][j]

  def East():
    for i in range(H):
      for j in reversed(range(W)):
        if a[i][j] == '.':
          k = j - 1
          while k >= 0 and a[i][k] == '.':
            k -= 1
          if k >= 0 and a[i][k] == 'O':
            a[i][j], a[i][k] = a[i][k], a[i][j]

  def Load():
    return sum(H - i for i, row in enumerate(a) for ch in row if ch == 'O')

  if not part2:
    North()
    return Load()

  def Key():
    return ''.join(''.join(row) for row in a)

  def Step():
    North()
    West()
    South()
    East()

  # Simulate until we find a cycle.
  seen = {}
  steps = 0
  while (key := ''.join(''.join(row) for row in a)) not in seen:
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

  return Load()

lines = sys.stdin.read().splitlines()
print(Solve(lines, False))  # part 1
print(Solve(lines, True))   # part 2
