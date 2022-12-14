#!/usr/bin/env python3

from random import choice, randint

dirs = 'UDLR'

for _ in range(10000000):
  x = randint(0, 1000)
  if x == 0:
    dist = 0
  elif x <= 10:
    dist = randint(0, 2000)
  else:
    dist = randint(0, 20)
  print(choice(dirs), dist)
