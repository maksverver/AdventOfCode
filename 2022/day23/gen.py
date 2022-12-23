#!/usr/bin/env python3

from random import uniform

p = 0.75
H = 200
W = 200

for r in range(H):
  print(''.join('.#'[uniform(0, 1) < p] for _ in range(W)))
