#!/usr/bin/env python3

from random import uniform, choice

H = 300
W = 500
p_empty = 0.15

print('#.' + W*'#')
for r in range(H):
  row = ['#']
  for c in range(W):
    if uniform(0, 1) < p_empty:
      row.append('.')
    elif c == 0 or c == W - 1:
      row.append(choice('<>'))
    else:
      row.append(choice('<>^v'))
  row.append('#')
  print(''.join(row))

print(W*'#' + '.#')
