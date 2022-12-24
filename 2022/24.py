# Advent of Code 2022 Day 24: Blizzard Basin
# https://adventofcode.com/2022/day/24

import sys

# Assume the grid is bordered by walls (except 2 openings for start and finish).
# Conveniently, there are no vertical blizzards in the starting/finishing column,
# avoiding ambiguity about whether a blizzard can move into the opening or not.
full_grid = sys.stdin.read().splitlines()
grid = [row[1:-1] for row in full_grid[1:-1]]
H, W = len(grid), len(grid[0])
start = (-1, full_grid[0].index('.') - 1)
finish = (H, full_grid[-1].index('.') - 1)

def Search(t, start, finish):
  seen = set()
  todo = []

  def Add(t, r, c):
    state = (t, r, c)
    if state not in seen:
      seen.add(state)
      todo.append(state)

  r, c = start
  Add(t, r, c)
  for t, r, c in todo:
    if 0 <= r < H:
      # Check if I'm hit by a blizzard.
      if grid[(r - t) % H][c] == 'v': continue
      if grid[(r + t) % H][c] == '^': continue
      if grid[r][(c - t) % W] == '>': continue
      if grid[r][(c + t) % W] == '<': continue
    Add(t + 1, r, c)  # wait in place
    for r2, c2 in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
      if (r2, c2) == finish:
        return t + 1
      if 0 <= r2 < H and 0 <= c2 < W:
        Add(t + 1, r2, c2)  # move

# Part 1: time from start to finish.
t1 = Search(0, start, finish)
print(t1)

# Part 2: time from start to finish, back to start, then back to finish.
t2 = Search(t1, finish, start)
t3 = Search(t2, start, finish)
print(t3)
