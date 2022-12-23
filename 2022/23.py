# Advent of Code 2022 Day 23: Unstable Diffusion
# https://adventofcode.com/2022/day/23

from collections import defaultdict
from math import inf
import sys

directions = [
  [(-1,  0), (-1, +1), (-1, -1)],  # N, NE, NW
  [(+1,  0), (+1, +1), (+1, -1)],  # S, SE, SW
  [( 0, -1), (-1, -1), (+1, -1)],  # W, NW, SW
  [( 0, +1), (-1, +1), (+1, +1)],  # E, NE, SE
]

def BoundingBox(coords):
  r1 = c1 = inf
  r2 = c2 = -inf
  for r, c in coords:
    r1 = min(r1, r)
    c1 = min(c1, c)
    r2 = max(r2, r)
    c2 = max(c2, c)
  return (r1, c1, r2 + 1, c2 + 1)


def HasNeighbors(positions, r, c):
  for dr in (-1, 0, 1):
    for dc in (-1, 0, 1):
      if (dr != 0 or dc != 0) and (r + dr, c + dc) in positions:
        return True
  return False


def UpdateStep(elves, round):
  proposals = defaultdict(list)
  for r, c in elves:
    if HasNeighbors(elves, r, c):
      for d in range(4):
        dirs = directions[(d + round) % len(directions)]
        if all((r + dr, c + dc) not in elves for (dr, dc) in dirs):
          # Propose a move
          dr, dc = dirs[0]
          proposals[r + dr, c + dc].append((r, c))
          break
  for dst, srcs in proposals.items():
    if len(srcs) == 1:
      elves.remove(srcs[0])
      elves.add(dst)


# def DebugPrint(elves, round):
#   print('Round', round)
#   r1, c1, r2, c2 = BoundingBox(elves)
#   for r in range(r1, r2):
#     print(''.join('.#'[(r, c) in elves] for c in range(c1, c2)))
#   print()


elves = set((r, c) for r, line in enumerate(sys.stdin) for c, ch in enumerate(line) if ch == '#')
last_elves = None
round = 0
while elves != last_elves:
  last_elves = set(elves)
  UpdateStep(elves, round)
  round += 1
  if round == 10:
    # Part 1
    r1, c1, r2, c2 = BoundingBox(elves)
    print((r2 - r1) * (c2 - c1) - len(elves))

# Part 2
print(round)
