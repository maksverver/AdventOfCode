#!/usr/bin/env python

import sys
from random import choice, sample, randint

size       =  9_999_999
last_value =  9_876_543
total_sum  =  474747474
alphabet = [chr(ch) for ch in range(33, 127)]  # 94 printable ASCII characters


# position[i] is the position before which we do not allow a distinct
# substring of i characters to be formed.
# while True:
#   positions = [0, 1] + sorted(sample(range(2, last_value), k=len(alphabet) - 3)) + [last_value]
#   extra_value = sum(positions) - total_sum
#   if 1 < extra_value < last_value:
#     positions.append(extra_value)
#     positions.sort()
#     assert len(set(positions)) == len(positions)
#     break

positions = [0, 1] + sorted(sample(range(2, last_value), k=len(alphabet) - 2)) + [last_value]

#positions = [0, 1] + sorted(sample(range(2, size), k=len(alphabet) - 1))
#assert len(positions) == len(alphabet) + 1

def Generate(positions):
  alphabet_set = set(alphabet)
  s = choice(alphabet)
  j = 2
  for i in range(1, size):
    assert i == len(s)
    if j == len(positions):
      s += choice(alphabet)
    else:
      if i == positions[j]:
        # Hack to fix the position exactly. Doesn't always work :/
        #print(i, j, s, len(s), s[i - j - j:i - j - 1])
        if j + 1 == len(positions):
          s = s[:i - j - 1] + choice(s[i - j - j:i - j - 1]) + ''.join(sample(alphabet, k=j))
        #print(i, j, s, len(s))
        j += 1
      suffix = s[-(j - 1):]
      suffix_set = set(suffix)
      if len(suffix_set) == j - 1:
        s += choice(suffix)
      else:
        #print(i, j, alphabet, suffix)
        s += choice(list(alphabet_set - suffix_set))
    if i % 100000 == 0:
      print('Progress: %.2f%%' % (100.0 * i / size), file=sys.stderr)
  return s

print(Generate(positions))
