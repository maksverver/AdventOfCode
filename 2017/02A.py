import sys

checksum = 0
for line in sys.stdin:
  numbers = [int(s) for s in line.split()]
  checksum += max(numbers) - min(numbers)
print(checksum)
