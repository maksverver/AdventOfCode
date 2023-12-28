# Advent of Code 2023 Day 1: Trebuchet?!
# https://adventofcode.com/2023/day/1

import sys

a = [s.strip() for s in sys.stdin]

def Solve(part2):

  def FindFirstDigit(s, i):
    if s[i].isdigit(): return int(s[i])
    if part2:
      if s.startswith('one',   i): return 1
      if s.startswith('two',   i): return 2
      if s.startswith('three', i): return 3
      if s.startswith('four',  i): return 4
      if s.startswith('five',  i): return 5
      if s.startswith('six',   i): return 6
      if s.startswith('seven', i): return 7
      if s.startswith('eight', i): return 8
      if s.startswith('nine',  i): return 9
    return FindFirstDigit(s, i + 1)

  def FindLastDigit(s, i):
    if s[i - 1].isdigit(): return int(s[i - 1])
    if part2:
      if s.endswith('one',   0, i): return 1
      if s.endswith('two',   0, i): return 2
      if s.endswith('three', 0, i): return 3
      if s.endswith('four',  0, i): return 4
      if s.endswith('five',  0, i): return 5
      if s.endswith('six',   0, i): return 6
      if s.endswith('seven', 0, i): return 7
      if s.endswith('eight', 0, i): return 8
      if s.endswith('nine',  0, i): return 9
    return FindLastDigit(s, i - 1)

  return sum(10*FindFirstDigit(s, 0) + FindLastDigit(s, len(s)) for s in a)

print(Solve(0))
print(Solve(1))
