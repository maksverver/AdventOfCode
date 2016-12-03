import sys

numbers = [map(int, line.split()) for line in sys.stdin]
for r in range(0, len(numbers), 3):
  a, b, c = numbers[r + 0]
  d, e, f = numbers[r + 1]
  g, h, i = numbers[r + 2]
  numbers[r + 0] = a, d, g
  numbers[r + 1] = b, e, h
  numbers[r + 2] = c, f, i
print sum(a + b > c for a, b, c in map(sorted, numbers))
