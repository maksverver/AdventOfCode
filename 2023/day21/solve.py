from collections import deque
import sys

# Finds distance from start to all other reachable cells when the grid is copied
# max_copies times in all four directions, keeping the original coordinates in
# the center.
#
# For example, if the grid is a 2x3 grid:
#
#   0
#   |
# 0-abc
#   def
#
# Then max_copies=2 creates a 6x9 grid. Note that the copy in the topleft corner
# has negative coordinates.
#
#   -3   0   3
#    |   |   |
# -2 abc abc abc
# -1 def def def
#
#  0 abc abc abc
#  1 def def def
#
#  2 abc abc abc
#  3 def def def
#
# Returns the distances as dict of {(r, c): distance}
def CalculateDistances(grid, max_copies):
  H = len(grid)
  W = len(grid[0])
  min_r = -max_copies*H
  min_c = -max_copies*W
  max_r = (max_copies + 1)*H
  max_c = (max_copies + 1)*W
  start, = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == 'S']
  todo = deque([(start, 0)])
  dist = {start: 0}
  while todo:
    (r1, c1), d = todo.popleft()
    for (r2, c2) in [(r1 - 1, c1), (r1, c1 - 1), (r1, c1 + 1), (r1 + 1, c1)]:
      if (grid[r2 % H][c2 % W] != '#' and
          min_r <= r2 < max_r and
          min_c <= c2 < max_c and
          (state := (r2, c2)) not in dist):
        dist[state] = d + 1
        todo.append((state, d + 1))
  return dist

def Part1(grid, total_steps):
  return sum(dist <= total_steps and dist % 2 == total_steps % 2
      for dist in CalculateDistances(grid, 0).values())


def DebugPrintReachable(grid, dist):
  for r, row in enumerate(grid):
    print(''.join('#' if ch == '#' else '.o'[(r,c) in dist] for c, ch in enumerate(row)))
  print()


def DebugPrintDistances(grid, dist, max_copies, o_r, o_c):
  assert grid[o_r][o_c] != '#'
  H = len(grid)
  W = len(grid[0])
  n = 2*max_copies + 1
  m = [[None]*n for _ in range(n)]
  for (r, c), d in dist.items():
    if r % H == o_r and c % W == o_c:
      y = r//H + max_copies
      x = c//W + max_copies
      if 0 <= x < n and 0 <= y < n:
        assert m[y][x] is None
        m[y][x] = d
  for row in m:
    print(''.join('%6d' % (i or 0) for i in row))
  print()

# Solves the problem for each origin point (r, c) with 0 < r ≤ H and 0 < c ≤ W
# individually.
#
# The idea is that because the input is surrounded by empty spaces and the input
# is square, there is a constant difference between the numbers in the same row
# and column, and between diagonals. For example for the test data:
#
#    112   101    90    79    68  |  67  |  68    79    90   101   112
#    101    90    79    68    57  |  56  |  57    68    79    90   101
#     90    79    68    57    46  |  45  |  46    57    68    79    90
#     79    68    57    46    35  |  34  |  35    46    57    68    79
#     68    57    46    35    24  |  23  |  24    35    46    57    68
#  -------------------------------+------+-------------------------------
#     63    52    41    28    13  |   2  |  17    32    45    56    67
#  -------------------------------+------+-------------------------------
#     64    53    42    31    20  |  19  |  28    39    50    61    72
#     75    64    53    42    31  |  34  |  39    50    61    72    83
#     86    75    64    53    42  |  45  |  50    61    72    83    94
#     97    86    75    64    53  |  56  |  61    72    83    94   105
#    108    97    86    75    64  |  67  |  72    83    94   105   116
#
# Since the input file is 11x11, the differences are eventually all 11
# (45 + 11 = 56, 56 + 11, 67, 67 + 78 = 11, etc.)
#
# The same on the diagonals. In the bottom left corner for example, we have
# 39 + 11 = 50. 50 + 11 = 61, 61 + 11 = 72 etc. So we can use that to
# efficiently calculate how many cells are below maximum distance.

def Part2(grid, total_steps, /, print_progress=False):
  H = len(grid)
  W = len(grid[0])

  # Determined experimentally. Increase if you get KeyError accessing dist[p]
  max_copies = 7
  dist = CalculateDistances(grid, max_copies)
  if print_progress: print('BFS complete', file=sys.stderr)

  #DebugPrintReachable(grid, dist)

  parity = total_steps % 2
  answer = 0
  for o_r in range(H):
    if print_progress:
      print('%5.2f%% complete' % (100.0 * o_r / H), file=sys.stderr)

    for o_c in range(W):
      o = o_r, o_c

      if o not in dist:
        # if grid[o_r][o_c] != '#': print(o, 'unreachable')
        continue

      #DebugPrintDistances(grid, dist, max_copies, o_r, o_c)

      assert grid[o_r][o_c] != '#'

      if dist[o] % 2 == parity and dist[o] <= total_steps:
        answer += 1

      def ScanOrtoghonal(dr, dc):
        nonlocal answer
        last_d = dist[o]
        deltas = []
        i = 0
        while True:
          i += 1
          p = (o_r + dr*H*i, o_c + dc*W*i)
          d = dist[p]
          if d > total_steps: break
          if d % 2 == parity: answer += 1
          deltas.append(d - last_d)
          last_d = d

          # Shortcut detection!
          if d % 2 == parity and len(deltas) >= 3 and deltas[-1] == deltas[-2] == deltas[-3]:
            delta = deltas[-1]
            assert delta % 2 == 1
            answer += (total_steps - d) // (2 * delta)
            break

      def ScanDiagonal(dr, dc):
        nonlocal answer
        k = 2
        deltas = []
        last_d = -1
        while True:
          points = [(o_r + dr*H*(i - k), o_c + dc*W*i) for i in range(1, k)]
          dists = [dist[p] for p in points]
          if min(dists) > total_steps: break

          for d in dists:
            if d <= total_steps and d % 2 == parity: answer += 1

          # Shortcut detection
          if min(dists) != max(dists):
            deltas.append(-1)
            last_d = -1
          else:
            d = dists[0]
            delta = -1 if last_d == -1 else d - last_d
            last_d = d
            deltas.append(delta)
            if delta != -1 and d % 2 == parity and len(deltas) >= 3 and deltas[-1] == deltas[-2] == deltas[-3]:
              assert delta % 2 == 1
              n = len(points) + 2
              assert n == k + 1
              # Now we want to do:
              #
              # d += 2*delta
              # while d <= total_steps:
              #   answer += n
              #   n += 2
              #   d += delta * 2
              #
              # Which we can optimize to:
              repeat = (total_steps - d) // (2 * delta)
              answer += repeat*(n + repeat - 1)
              break

          k += 1

      for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        ScanOrtoghonal(dr, dc)

      for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        ScanDiagonal(dr, dc)

  #print('answer:',answer)
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

assert Part1(sample_grid, 6) == 16

assert Part2(sample_grid,    6) ==       16
assert Part2(sample_grid,   10) ==       50
assert Part2(sample_grid,   50) ==     1594
assert Part2(sample_grid,  100) ==     6536
assert Part2(sample_grid,  500) ==   167004
assert Part2(sample_grid, 1000) ==   668697
assert Part2(sample_grid, 5000) == 16733044

grid = [line.strip() for line in sys.stdin]
print(Part1(grid, 64))
print(Part2(grid, 26501365))
