from copy import deepcopy
import sys

def ParseBoxes(boxes):
  lines = boxes.splitlines()
  stacks = []
  for col, label in enumerate(lines[-1]):
    if label.isspace():
      continue
    assert int(label) == len(stacks) + 1
    stack = []
    for row in range(len(lines) - 2, -1, -1):
      box = lines[row][col]
      if box.isspace():
        break
      stack.append(box)
    stacks.append(stack)
  return stacks


def ParseInstruction(i):
  move, count, from_, src, to_, dst = i.split()
  assert move == 'move' and from_ == 'from' and to_ == 'to'
  return int(count), int(src) - 1, int(dst) - 1


def Solve(stacks, reverse):
  for n, i, j in instructions:
    assert i != j
    boxes = stacks[i][-n:]
    stacks[i] = stacks[i][:-n]
    stacks[j] += reversed(boxes) if reverse else boxes
  return ''.join(stack[-1] for stack in stacks)


part1, part2 = sys.stdin.read().split('\n\n')
stacks = ParseBoxes(part1)
instructions = list(map(ParseInstruction, part2.splitlines()))

print(Solve(deepcopy(stacks), reverse=True))
print(Solve(deepcopy(stacks), reverse=False))
