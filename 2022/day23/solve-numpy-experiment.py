# Advent of Code 2022 Day 23: Unstable Diffusion
# https://adventofcode.com/2022/day/23

# Hackier but faster version of solve-numpy.py

import numpy as np
import sys

# North, South, West, East
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def Trim(elves):
  top = left = 0
  bottom = 0
  right = 0
  while not np.any(elves[top]): top += 1
  while not np.any(elves[-1 - bottom]): bottom += 1
  while not np.any(elves[:, left]): left += 1
  while not np.any(elves[:, -1 - right]): right += 1
  H, W = elves.shape

  if top > 1: elves = elves[top - 1:]
  if bottom > 1: elves = elves[:H - (bottom - 1)]
  if left > 1: elves = elves[:, left - 1:]
  if right > 1: elves = elves[:, :W - (right - 1)]

  top = 1 - min(top, 1)
  bottom = 1 - min(bottom, 1)
  left = 1 - min(left, 1)
  right = 1 - min(right, 1)
  if top > 0 or bottom > 0 or left > 0 or right > 0:
    return np.pad(elves, ((top, bottom), (left, right)))
  else:
    return elves

def NextStep(padded_elves, round):
  H, W = padded_elves.shape
  H -= 2
  W -= 2
  inner_elves = padded_elves[1:H + 1, 1:W + 1]

  # nn[r][c] == True if there is an elf due north of (r, c), etc.
  nn = padded_elves[0:H    , 1:W + 1]
  ss = padded_elves[2:H + 2, 1:W + 1]
  ww = padded_elves[1:H + 1, 0:W    ]
  ee = padded_elves[1:H + 1, 2:W + 2]
  nw = padded_elves[0:H    , 0:W    ]
  ne = padded_elves[0:H    , 2:W + 2]
  sw = padded_elves[2:H + 2, 0:W    ]
  se = padded_elves[2:H + 2, 2:W + 2]

  neighbor_count = np.add.reduce([nn, ss, ee, ww, ne, nw, se, sw])

  # Elves without neighbors stay put.
  next_elves = inner_elves & (neighbor_count == 0)
  undecided = inner_elves ^ next_elves

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
  padded_conflict_count = np.add.reduce([
    np.pad(want_move[d], ((1 + dr, 1 - dr), (1 + dc, 1 - dc)))
    for d, (dr, dc) in enumerate(DIRS)
  ])

  padded_next_elves = np.pad(next_elves, (1, 1))

  for d, (dr, dc) in enumerate(DIRS):
    can_move = want_move[d] & (padded_conflict_count[1+dr:H+1+dr, 1+dc:W+1+dc] == 1)
    padded_next_elves |= np.pad(can_move, ((1 + dr, 1 - dr), (1 + dc, 1 - dc)))
    cannot_move = want_move[d] ^ can_move
    padded_next_elves[1:-1,1:-1] |= cannot_move

  return Trim(padded_next_elves)

elves = Trim(np.array([[ch == '#' for ch in line] for line in sys.stdin.read().splitlines()]))

last_elves = None
round = 0
while not np.array_equal(elves, last_elves):
  last_elves = elves
  elves = NextStep(elves, round)
  round += 1

  if round == 10:
    # Part 1
    H, W = elves.shape
    print((H - 2) * (W - 2) - np.sum(elves))

# Part 2
print(round)
