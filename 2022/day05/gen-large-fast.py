#!/usr/bin/env python3

from lib05 import CalculateLocations, WriteTestInput
from math import ceil, sqrt
from copy import deepcopy
from random import choices, randint
import sys

# width = 9
# max_height = 20000
# num_instructions = 20000
# word1 = 'GATHERING'
# word2 = 'DEVSCHUUR'

# width = 9
# max_height = 1_500_000
# num_instructions = 1_500_000
# word1 = 'KERSTBOOM'
# word2 = 'HENKLEEFT'

width = 5_000
max_height = 5_000
num_instructions = 4_000_000
answer1 = open('neuromancer.txt').read(width)
answer2 = open('christmas-carol.txt').read(width)

assert(len(answer1) == width)
assert(len(answer2) == width)


def GenStack(len):
  return [chr(randint(ord('A'), ord('Z'))) for _ in range(len)]

def Main():
  heights = [randint(max(1, max_height - 20), max_height) for _ in range(width)]
  stacks = [GenStack(h) for h in heights]

  instructions = []
  for i in range(num_instructions):
    if i % 1000 == 0:
      print('%.2f%% complete' % (100.0 * i / num_instructions), file=sys.stderr)
    # Pick a random stack to move from (must have at least 1 box)
    # Prefer selecting higher stacks.
    i, = choices(list(range(width)), weights=[h - 1 for h in heights])
    # Pick a random stack to move to (but not the same as moving from)
    if (j := randint(0, width - 2)) >= i: j = j + 1
    # Pick number of boxes to move (at least 1, but never all)
    n = randint(1, heights[i] - 1)
    heights[i] -= n
    heights[j] += n
    instructions.append((n, i, j))

  for (reverse, answer) in [(True, answer1), (False, answer2)]:
    locations = CalculateLocations(stacks, instructions, reverse=reverse)
    for stack, locations in zip(stacks, locations):
      for pos, label in locations:
        stack[pos] = answer[label]

  WriteTestInput(stacks, instructions)

Main()
