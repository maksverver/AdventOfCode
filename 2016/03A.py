import sys

numbers = [map(int, line.split()) for line in sys.stdin]
print sum(a + b > c for a, b, c in map(sorted, numbers))
