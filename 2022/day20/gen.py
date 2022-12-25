#!/usr/bin/env python3

import sys
from random import randint

def Generate(N, file=sys.stdout):
  min_value = -3*N
  max_value = 5*N

  # Make sure result is composed of different elements
  assert 1000 % N != 2000 % N != 3000 % N

  def RandomValue():
    i = randint(min_value, max_value - 1)
    if i == 0: i += 1
    return i

  numbers = [RandomValue() for i in range(N)]
  numbers[randint(0, N - 1)] = 0
  for number in numbers:
    print(number, file=file)

def GenerateFile(filename, N):
  with open(filename, 'wt') as file:
    Generate(N, file=file)

GenerateFile('large-1.txt',    25_000)
GenerateFile('large-2.txt',   150_000)
GenerateFile('large-3.txt', 1_000_000)
