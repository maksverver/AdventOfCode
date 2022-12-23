# Advent of Code 2022 Day 23: Unstable Diffusion
# https://adventofcode.com/2022/day/23

import numpy as np
import sys

# North, South, West, East
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def Trim(elves):
  top = left = 0
  bottom, right = elves.shape
  while not np.any(elves[top]): top += 1
  while not np.any(elves[bottom - 1]): bottom -= 1
  while not np.any(elves[:, left]): left += 1
  while not np.any(elves[:, right - 1]): right -= 1
  return elves[top:bottom, left:right]

def Rotate(a, dr, dc):
  if dr != 0: a = np.roll(a, dr, axis=0)
  if dc != 0: a = np.roll(a, dc, axis=1)
  return a

def NextStep(old_elves, round):
  elves = np.pad(old_elves, (1, 1))

  # nn[r][c] == True if there is an elf due north of (r, c), etc.
  nn = np.pad(old_elves, ((2, 0), (1, 1)))
  ss = np.pad(old_elves, ((0, 2), (1, 1)))
  ww = np.pad(old_elves, ((1, 1), (2, 0)))
  ee = np.pad(old_elves, ((1, 1), (0, 2)))
  nw = np.pad(old_elves, ((2, 0), (2, 0)))
  ne = np.pad(old_elves, ((2, 0), (0, 2)))
  sw = np.pad(old_elves, ((0, 2), (2, 0)))
  se = np.pad(old_elves, ((0, 2), (0, 2)))

  neighbor_count = np.add.reduce([nn, ss, ee, ww, ne, nw, se, sw])

  # Elves without neighbors stay put.
  next_elves = elves & (neighbor_count == 0)
  undecided = elves ^ next_elves

  # Find the direction each of the undecided elves wants to move in.
  want_move = 4*[None]
  tests = [
    (0, nn | ne | nw), # north
    (1, ss | se | sw), # south
    (2, ww | nw | sw), # west
    (3, ee | ne | se), # east
  ]
  for d, test in tests[round % 4:] + tests[:round % 4]:
    cant_move = undecided & test
    want_move[d] = undecided & ~cant_move
    undecided &= cant_move

  # Any remaining elves have no space to move in any direction and will stay put.
  next_elves |= undecided

  # Count conflicting destinations
  conflict_count = np.add.reduce([Rotate(want_move[d], dr, dc) for d, (dr, dc) in enumerate(DIRS)])

  for d, (dr, dc) in enumerate(DIRS):
    can_move = want_move[d] & (Rotate(conflict_count, -dr, -dc) == 1)
    next_elves |= Rotate(can_move, dr, dc)
    cannot_move = want_move[d] ^ can_move
    next_elves |= cannot_move

  return Trim(next_elves)

elves = np.array([[ch == '#' for ch in line] for line in sys.stdin.read().splitlines()])

last_elves = None
round = 0
while not np.array_equal(elves, last_elves):
  last_elves = elves
  elves = NextStep(elves, round)
  round += 1

  if round == 10:
    # Part 1
    H, W = elves.shape
    print(H * W - np.sum(elves))


# Part 2
print(round)
