from random import randint, random

def GenCase():
  n = randint(1, 1000)
  s = ''.join('.#'[random() < 0.8] for _ in range(n))
  t = ''.join((ch, '?')[random() < 0.4] for ch in s)
  runs = []
  i = 0
  while i < len(s):
    if s[i] == '#':
      j = i + 1
      while j < len(s) and s[j] == '#':
        j += 1
      runs.append(j - i)
      i = j
    i = i + 1
  return t, runs

for _ in range(1000):
  t, runs = GenCase()
  while not runs:
    t, runs = GenCase()

  print(t, ','.join(map(str, runs)))
