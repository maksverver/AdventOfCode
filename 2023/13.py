# Advent of Code 2023 Day 13: Point of Incidence
# https://adventofcode.com/2023/day/13

import sys

def CheckReflection(a, j, max_errors):
  '''Returns the number of errors we see when reflecting matrix `a` vertically,
     using the horizontal line of reflection between rows (j - 1) and (j).'''
  h = len(a)
  w = len(a[0])
  i = j - 1
  errors = 0
  while i >= 0 and j < h:
    for k in range(w):
      if a[i][k] != a[j][k]:
        errors += 1
        if errors > max_errors: break  # optimization
    i -= 1
    j += 1
  return errors


def Solve(patterns, errors):
  answer = 0
  for a in patterns:
    b = list(zip(*a))  # transpose a
    res, = (
        list(100*r for r in range(1, len(a)) if CheckReflection(a, r, errors) == errors) +
        list(    c for c in range(1, len(b)) if CheckReflection(b, c, errors) == errors))
    answer += res
  return answer


# Input
patterns = [part.split('\n') for part in sys.stdin.read().strip().split('\n\n')]

print(Solve(patterns, 0))  # part 1
print(Solve(patterns, 1))  # part 2
