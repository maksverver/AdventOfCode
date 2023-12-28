# Advent of Code 2023 Day 12: Hot Springs
# https://adventofcode.com/2023/day/12

from functools import cache
import sys


def CountCombinations(s, runs):
  '''Returns the number of ways question marks in `s` can be filled in
     consistent with `runs`. `s` must have an extra '.' appended.'''

  @cache
  def Calc(i, j):
    '''Returns number of solutions to s[i:] using runs[j:].'''
    if j == len(runs):
      return '#' not in s[i:]

    n = runs[j]
    if len(s) - i < n + 1:
      return 0

    res = 0
    if s[i] != '#':
      res += Calc(i + 1, j)
    if '.' not in s[i:i + n] and s[i + n] != '#':
      res += Calc(i + n + 1, j + 1)
    return res

  return Calc(0, 0)


def Solve(records):
  return sum(CountCombinations(s + '.', runs) for s, runs in records)


def ParseLine(line):
  '''Parses a line like "???.### 1,1,3" into a pair ("???.###", [1, 1, 3]).'''
  a, b = line.split()
  return a, list(map(int, b.split(',')))


# Part 1
records1 = [ParseLine(line) for line in sys.stdin]
print(Solve(records1))

# Part 2
records2 = [('?'.join([s]*5), runs*5) for (s, runs) in records1]
print(Solve(records2))
