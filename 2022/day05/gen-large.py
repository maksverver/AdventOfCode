#!/usr/bin/env python3

# Generates a large random data set. See gen-large-fast.py for a faster version
# that can generate much bigger data sets.

from lib05 import WriteTestInput
from math import sqrt
from copy import deepcopy
from random import choices, randint
import sys

width = 9
max_height = 20000
num_instructions = 20000

def Move(stacks, n, i, j, reverse):
  assert i != j
  boxes = stacks[i][-n:]
  stacks[i] = stacks[i][:-n]
  stacks[j] += reversed(boxes) if reverse else boxes


def GenStack(len):
  return [chr(randint(ord('A'), ord('Z'))) for _ in range(len)]


def Main():
  stacks = [GenStack(randint(1, max_height)) for _ in range(width)]
  stacks1 = deepcopy(stacks)
  stacks2 = deepcopy(stacks)

  instructions = []
  for _ in range(num_instructions):
    # Pick a random stack to move from (must have at least 1 box)
    # Prefer selecting higher stacks.
    i, = choices(list(range(width)), weights=[len(s) - 1 for s in stacks1])
    # Pick a random stack to move to (but not the same as moving from)
    if (j := randint(0, width - 2)) >= i: j = j + 1
    # Pick number of boxes to move (at least 1, but never all)
    n = randint(1, len(stacks1[i]) - 1)
    Move(stacks1, n, i, j, reverse=True)
    Move(stacks2, n, i, j, reverse=False)
    instructions.append((n, i, j))

  # Print solution to stderr
  print(''.join(stack[-1] for stack in stacks1), file=sys.stderr)
  print(''.join(stack[-1] for stack in stacks2), file=sys.stderr)

  WriteTestInput(stacks, instructions)

Main()
