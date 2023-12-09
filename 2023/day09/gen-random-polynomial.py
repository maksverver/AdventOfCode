from random import randint, shuffle
import sys

answer1 = 0
answer2 = 0

sizes = list(range(1, 50))
shuffle(sizes)

for size in sizes:
  coefficients = [randint(-10, 10) for _ in range(size)]
  def Eval(x):
    return sum(a*(x**i) for i, a in enumerate(coefficients))
  start = -(size // 2)
  answer1 += Eval(start + size)
  answer2 += Eval(start - 1)
  print(*[Eval(start + i) for i in range(size)])

print(answer1, file=sys.stderr)
print(answer2, file=sys.stderr)
