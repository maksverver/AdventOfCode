import sys

num_valid = 0
for line in sys.stdin:
  words = line.split()
  num_valid += len(words) == len(set(words))
print(num_valid)
