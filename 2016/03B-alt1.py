import sys

numbers = [list(map(int, line.split())) for line in sys.stdin]
for r in range(0, len(numbers), 3):
  numbers[r:r+3] = zip(*numbers[r:r+3])
print(sum(a + b > c for a, b, c in map(sorted, numbers)))
