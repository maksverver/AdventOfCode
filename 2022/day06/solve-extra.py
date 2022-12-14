# Day 6 extra challenge:
#
# Given a file with up to 94 different characters, instead of just 26.
#
# Let's define p(x) as the end position of the first occurrence of a substring
# of length x where all characters are different. The original problem asked us
# to find p(4) and p(14).
#
# For this problem:
#
#  Part 1: find p(94)
#  Part 2: find sum of p(x) for 1 <= x <= 94
#

import sys

def Solve(s):
  k = 1
  total = 0
  last = 0
  char_count = {}

  def Add(ch):
    if ch not in char_count:
      char_count[ch] = 1
    else:
      char_count[ch] += 1

  def Remove(ch):
    char_count[ch] -= 1
    if char_count[ch] == 0:
      del char_count[ch]

  for i, ch in enumerate(s):
    Add(ch)
    if len(char_count) == k:
      #print(k, i + 1)
      last = i + 1
      total += last
      k = k + 1
    else:
      Remove(s[i - k + 1])

  assert k == 95
  print(last)
  print(total)

total = 0
s = sys.stdin.readline().strip()
Solve(s)
