from collections import deque
import sys

def Solve(grid, total_steps):
  H = len(grid)
  W = len(grid[0])
  answer = 0
  start, = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == 'S']
  todo = deque([(start, 0)])
  dist = {start: 0}
  while todo:
    (r1, c1), d = todo.popleft()
    if d % 2 == total_steps % 2:
      answer += 1
    if d < total_steps:
      for (r2, c2) in [(r1 - 1, c1), (r1, c1 - 1), (r1, c1 + 1), (r1 + 1, c1)]:
        if grid[r2 % H][c2 % W] != '#' and (state := (r2, c2)) not in dist:
          dist[state] = d + 1
          todo.append((state, d + 1))
  return answer


sample_grid = '''
  ...........
  .....###.#.
  .###.##..#.
  ..#.#...#..
  ....#.#....
  .##..S####.
  .##..#...#.
  .......##..
  .##.#.####.
  .##..##.##.
  ...........
'''.split()

assert Solve(sample_grid,    6) ==       16
assert Solve(sample_grid,   10) ==       50
assert Solve(sample_grid,   50) ==     1594
assert Solve(sample_grid,  100) ==     6536
# These also work but are slow
# assert Solve(sample_grid,  500) ==   167004
# assert Solve(sample_grid, 1000) ==   668697
# assert Solve(sample_grid, 5000) == 16733044

grid = [line.strip() for line in sys.stdin]
print(Solve(grid, 1000))
print(Solve(grid, 5000))
