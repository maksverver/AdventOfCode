# Advent of Code 2023 Day 2: Cube Conundrum
# https://adventofcode.com/2023/day/2

import sys

answer1 = 0
answer2 = 0
for line in sys.stdin:
  line = line.strip()
  s1, s2 = line.split(': ')
  game, id = s1.split()
  assert game == 'Game'
  max_r = max_g = max_b = 0
  for round in s2.split('; '):
    r = g = b = 0
    for part in round.split(', '):
      n, col = part.split()
      n = int(n)
      assert col in ('red', 'green', 'blue')
      if col == 'red':   assert r == 0; r = n
      if col == 'green': assert g == 0; g = n
      if col == 'blue':  assert b == 0; b = n
    max_r = max(max_r, r)
    max_g = max(max_g, g)
    max_b = max(max_b, b)
  if max_r <= 12 and max_g <= 13 and max_b <= 14: answer1 += int(id)
  answer2 += max_r * max_g * max_b
print(answer1)
print(answer2)
