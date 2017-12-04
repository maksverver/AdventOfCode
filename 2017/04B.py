import sys

num_valid = 0
for line in sys.stdin:
  words = line.split()
  num_valid += len(words) == len(set(tuple(sorted(word)) for word in words))
print(num_valid)
