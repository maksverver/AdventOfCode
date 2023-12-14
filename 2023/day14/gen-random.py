from random import random

def GenChar():
  r = random()
  if r < 0.70: return '.'
  if r < 0.80: return 'O'
  return '#'

h, w = 320, 240
#h, w = 1000, 500
#h, w = 3000, 2000

for _ in range(h):
  print(''.join(GenChar() for _ in range(w)))
