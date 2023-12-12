from functools import cache
import sys

def CountCombinations(s, nums):
  '''Returns the number of question marks in `s` (which must have a terminating
    '.' appended), can be filled in consistent with `nums`.`'''

  @cache
  def CanExtend(i, n):
    if i == len(s): return False
    if n == 0: return s[i] in '.?'
    return s[i] in '#?' and CanExtend(i + 1, n - 1)

  @cache
  def Calc(i, j):
    if i == len(s): return j == len(nums)
    res = 0
    if s[i] in '.?':
      res += Calc(i + 1, j)
    if s[i] in '#?' and j < len(nums):
      n = nums[j]
      if CanExtend(i, n):
        res += Calc(i + n + 1, j + 1)
    return res

  return Calc(0, 0)


def Solve(records):
  return sum(CountCombinations(s + '.', nums) for s, nums in records)


def ParseLine(line):
  '''Parses a line like "???.### 1,1,3" into a pair ("???.###", [1, 1, 3]).'''
  a, b = line.split()
  return a, list(map(int, b.split(',')))

# Part 1
records1 = [ParseLine(line) for line in sys.stdin]
print(Solve(records1))

# Part 2
records2 = [('?'.join([s]*5), nums*5) for (s, nums) in records1]
print(Solve(records2))
