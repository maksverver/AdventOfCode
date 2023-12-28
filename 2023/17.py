# Advent of Code 2023 Day 17: Clumsy Crucible
# https://adventofcode.com/2023/day/17

from collections import defaultdict
from heapq import heappush, heappop
from math import inf
import sys

# Must be ordered in a circle! (see NextStates())
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

grid = [list(map(int, s.strip())) for s in sys.stdin]
H = len(grid)
W = len(grid[0])

def Solve(min_repeat, max_repeat):
  # Find the shortest path using Dijkstra's algorithm.
  #
  # States are of the form: (row, column, last direction % 2)
  # with a direction -1 as a special case for the start state.
  start_state = (0, 0, -1)

  end_states = {(H-1, W-1, dir) for dir in (0, 1)}

  # Given a (state, loss) pair, calculates the next (state, loss) pairs.
  def NextStates(state, loss):
    r, c, dir = state
    for dir2 in ((dir - 1) % 4, (dir + 1) % 4) if dir >= 0 else range(len(DIRS)):
      loss2 = loss
      r2, c2 = r, c
      dr, dc = DIRS[dir2]
      for i in range(max_repeat):
        r2 += dr
        c2 += dc
        if r2 < 0 or r2 >= H or c2 < 0 or c2 >= W: break
        loss2 += grid[r2][c2]
        if i + 1 >= min_repeat: yield ((r2, c2, dir2 % 2), loss2)

  # Core of Dijkstra's algorithm: find minimum loss per state.
  dist = defaultdict(lambda: inf)
  dist[start_state] = 0
  todo = [(0, start_state)]
  while todo:
    d, v = heappop(todo)
    if d > dist[v]: continue
    if v in end_states: return d
    for w, e in NextStates(v, d):
      if e < dist[w]:
        dist[w] = e
        heappush(todo, (e, w))

print(Solve(0,  3))  # Part 1
print(Solve(4, 10))  # Part 2
