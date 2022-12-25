#!/usr/bin/env python3

from random import uniform

def Gen(filename, p, H, W):
  with open(filename, 'wt') as f:
    for r in range(H):
      print(''.join('.#'[uniform(0, 1) < p] for _ in range(W)), file=f)

Gen('large-1.txt', 0.50, 100, 200)
Gen('large-2.txt', 0.75, 200, 200)
Gen('large-3.txt', 0.95, 200, 200)
Gen('large-4.txt', 0.50, 400, 400)
Gen('large-5.txt', 0.75, 400, 400)
