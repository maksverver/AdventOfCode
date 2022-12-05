from lib05 import *
from copy import deepcopy
import sys

def Solve(stacks, reverse):
  for n, i, j in instructions:
    assert i != j
    boxes = stacks[i][-n:]
    stacks[i] = stacks[i][:-n]
    stacks[j] += reversed(boxes) if reverse else boxes
  return ''.join(stack[-1] for stack in stacks)


part1, part2 = sys.stdin.read().split('\n\n')
stacks = ParseStacks(part1)
instructions = ParseInstructions(part2)

print(Solve(deepcopy(stacks), reverse=True))
print(Solve(deepcopy(stacks), reverse=False))
