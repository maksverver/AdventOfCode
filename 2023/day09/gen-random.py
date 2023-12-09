from random import randint, shuffle
import sys

sizes = list(range(1, 100))
shuffle(sizes)
cases = [[randint(0, 99) for _ in range(n)] for n in sizes]
for row in cases:
  print(*row)
