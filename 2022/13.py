from functools import cmp_to_key
import sys
import json

def ParsePart(part):
  a, b = part.splitlines()
  return json.loads(a), json.loads(b)

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
  return sum(i for i, (a, b) in enumerate(pairs, 1) if Compare(a, b) < 0)


def SolvePart2():
  marker1 = [[2]]
  marker2 = [[6]]
  items = [item for pair in pairs for item in pair]
  items.append(marker1)
  items.append(marker2)
  items.sort(key=cmp_to_key(Compare))
  return (items.index(marker1) + 1)*(items.index(marker2) + 1)


print(SolvePart1())
print(SolvePart2())
