from functools import cmp_to_key
import sys

def ParseLine(line):
  stack = [[]]
  i = 0
  while i < len(line):
    ch = line[i]
    if ch.isdigit():
      j = i + 1
      while line[j].isdigit():
        j += 1
      stack[-1].append(int(line[i:j]))
      i = j
    else:
      if ch == '[':
        stack.append([])
      elif ch == ']':
        stack[-2].append(stack.pop())
      else:
        assert ch == ','
      i = i + 1
  assert len(stack) == 1 and len(stack[0]) == 1
  return stack[0][0]

def ParsePart(part):
  a, b = part.splitlines()
  return ParseLine(a), ParseLine(b)

pairs = list(map(ParsePart, sys.stdin.read().split('\n\n')))


def Compare(a, b):
  if isinstance(a, int) and isinstance(b, int):
    return a - b

  if isinstance(a, int):
    return Compare([a], b)

  if isinstance(b, int):
    return Compare(a, [b])

  assert isinstance(a, list) and isinstance(b, list)
  for x, y in zip(a, b):
    if c := Compare(x, y):
      return c

  return len(a) - len(b)


def SolvePart1():
  # For debugging:
#  for i, (a, b) in enumerate(pairs, 1):
#    if Compare(a, b) < 0:
#      print(i, file=sys.stderr)
  return sum(i for i, (a, b) in enumerate(pairs, 1) if Compare(a, b) < 0)


def SolvePart2():
  marker1 = [[2]]
  marker2 = [[6]]
  lists = [list for pair in pairs for list in pair]
  i1 = sum(Compare(list, marker1) < 0 for list in lists)
  i2 = sum(Compare(list, marker2) < 0 for list in lists)
  return (i1 + 1) * (i2 + 2)

sys.setrecursionlimit(1000000)
print(SolvePart1())
print(SolvePart2())
sys.exit()
