import sys

first_free = None
total_free = 0
next_free = 0
for (first, last) in sorted(list(map(int, line.split('-'))) for line in sys.stdin):
  if next_free < first:
    if first_free is None:
      first_free = next_free
    total_free += first - next_free
  next_free = max(next_free, last + 1)
print(first_free)  # Part 1
print(total_free)  # Part 2
