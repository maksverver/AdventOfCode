#!/usr/bin/env python

from random import randint

H = 20
W = 10

def RandChar(a, b):
  return chr(randint(ord(a), ord(b)))

maze = [[RandChar('a', 'a') for _ in range(W)] for _ in range(H)]
maze[H - 1][randint(0,W-1)] = 'S'
maze[0][randint(0, W-1)] = 'E'
for line in maze:
  print(''.join(line))
for r in range(H, 10):
  cc = randint(0, W)
  for c in range(W):
    if c != cc:
      maze[r][c] = 'z'

