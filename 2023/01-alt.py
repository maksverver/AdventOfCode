# Advent of Code 2023 Day 1: Trebuchet?!
# https://adventofcode.com/2023/day/1

import sys

a = sys.stdin.read().splitlines()

def Solve(part2):
  words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']*part2

  def FindFirstDigit(s):
    for i in range(len(s)):
      if s[i].isdigit(): return int(s[i])
      for digit, word in enumerate(words, 1):
        if s.startswith(word, i): return digit

  def FindLastDigit(s):
    for i in reversed(range(len(s))):
      if s[i].isdigit(): return int(s[i])
      for digit, word in enumerate(words, 1):
        if s.startswith(word, i): return digit

  return sum(10*FindFirstDigit(s) + FindLastDigit(s) for s in a)

print(Solve(0))
print(Solve(1))
