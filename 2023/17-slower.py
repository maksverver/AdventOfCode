from collections import defaultdict
from heapq import heappush, heappop
from math import inf
import sys

# Order matters so we can detect reversal (see NextStates())
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

grid = [list(map(int, s.strip())) for s in sys.stdin]
H = len(grid)
W = len(grid[0])

def Solve(min_repeat, max_repeat):
  # Find the shortest path using Dijkstra's algorithm.
  #
  # States are of the form: (row, column, direction, repeat), where `repeat` is
  # the number of times the cart has been pushed in the same direction.
  start_state = (0, 0, -1, 0)

  # Given a (state, loss) pair, calculates the next (state, loss) pairs.
  def NextStates(state, loss):
    r, c, dir, repeat = state
    for dir2, (dr, dc) in enumerate(DIRS):
      if repeat == 0 or (
          # Minimum/maximum number of pushes in the same direction
          (repeat >= min_repeat if dir2 != dir else repeat < max_repeat) and
          # Important detail: can't reverse the cart!
          dir2 != (dir + 2)%4):
        r2 = r + dr
        c2 = c + dc
        if 0 <= r2 < H and 0 <= c2 < W:
          repeat2 = repeat + 1 if dir2 == dir else 1
          yield ((r2, c2, dir2, repeat2), loss + grid[r2][c2])

  # Core of Dijkstra's algorithm: find minimum loss per state.
  dist = defaultdict(lambda: inf)
  dist[start_state] = 0
  todo = [(0, start_state)]
  while todo:
    d, v = heappop(todo)
    if d > dist[v]: continue
    for w, e in NextStates(v, d):
      if e < dist[w]:
        dist[w] = e
        heappush(todo, (e, w))

  # Retrieve the solution.
  return min(loss for (r, c, dir, repeat), loss in dist.items()
      if r == H - 1 and c == W - 1 and repeat >= min_repeat)

print(Solve(0,  3))  # Part 1
print(Solve(4, 10))  # Part 2
