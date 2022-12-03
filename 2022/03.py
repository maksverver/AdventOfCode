from functools import reduce
import sys

def SplitInHalf(line):
  n = len(line)
  assert len(line) % 2 == 0
  n //= 2
  return [line[:n], line[n:]]

def SplitInGroups(lines, k):
  assert len(lines) % k == 0
  return [lines[i:i + k] for i in range(0, len(lines), k)]

def FindCommonChar(lines):
  ch, = reduce(lambda a, b: a.intersection(b), map(set, lines))
  return ch

def GetPrio(ch):
  return 1 + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ch)

lines = [line.strip() for line in sys.stdin]

# Part 1
print(sum(GetPrio(FindCommonChar(SplitInHalf(s))) for s in lines))

# Part 2
print(sum(GetPrio(FindCommonChar(group)) for group in SplitInGroups(lines, 3)))
