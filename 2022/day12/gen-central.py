#!/usr/bin/env python3

from random import choices
from math import *

chars = "abcdefghijklmnopqrstuvwxyz"

def Chr(h):
  assert 0 < h <= 26
  return chars[h]

#spread = 4
spread = 2
N = 1001
for r in range(N):
  row = []
  for c in range(N):
    dist = abs(r - N//2) + abs(c - N // 2)
    i = 26 - 26 * dist / N
    weights = [max(0, spread - abs(j - i)) for j in range(26)]
    ch, = choices(chars, weights=weights)
    #ch = chr(ord('z') - (26 * dist // N))
    row.append(ch)
  if r == 0:
    row[0] = 'S'
  if r == N // 2:
    row[N//2] = 'E'
  print(''.join(row))
