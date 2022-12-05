from lib05 import *
from copy import deepcopy
import sys

def Solve(stacks, reverse):
  locations = CalculateLocations(stacks, instructions, reverse)

  # Reconstruct answer
  answer = [None]*len(stacks)
  for stack, locations in zip(stacks, locations):
    for pos, label in locations:
      answer[label] = stack[pos]
  return ''.join(answer)


print('Reading input...', file=sys.stderr)
part1, part2 = sys.stdin.read().split('\n\n')

print('Parsing input...', file=sys.stderr)
stacks = ParseStacks(part1)
instructions = ParseInstructions(part2)

print('Solving part 1...', file=sys.stderr)
print(Solve(deepcopy(stacks), reverse=True))

print('Solving part 2...', file=sys.stderr)
print(Solve(deepcopy(stacks), reverse=False))
