from collections import defaultdict
import sys

orbiters = defaultdict(list)
for line in sys.stdin:
    a, b = line.strip().split(')')
    orbiters[a].append(b)

def CountOrbits(a, depth):
    return depth + sum(CountOrbits(b, depth + 1) for b in orbiters[a])

print(CountOrbits('COM', 0))
