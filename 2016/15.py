import re
import sys

# disks is a list of (disc number, size, initial-position) triples.
# This function assumes disc sizes are co-prime.
def Calculate(disks):
  period, offset = 1, 0
  for disk, size, position in disks:
    while (position + disk + offset)%size != 0:
      offset += period
    period *= size
  return offset

pattern = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).')

def Parse(line):
  return map(int, pattern.match(line).groups())

disks = map(Parse, sys.stdin)
print Calculate(disks)
disks += [(7, 11, 0)]
print Calculate(disks)
