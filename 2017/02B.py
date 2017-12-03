import sys

checksum = 0
for line in sys.stdin:
  numbers = [int(s) for s in line.split()]
  for i, x in enumerate(numbers):
    for j, y in enumerate(numbers):
      if i != j and x%y == 0:
        checksum += x//y
print(checksum)
