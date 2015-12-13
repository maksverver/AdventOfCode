from collections import defaultdict
from itertools import permutations
import sys

diff = defaultdict(lambda: dict())

def Evaluate(names, wraparound = True):
	return sum(
		diff[names[i - 1]][names[i]] + diff[names[i]][names[i - 1]]
		for i in range(1 - wraparound , len(names)))

for line in sys.stdin:
	a, would, verb, n, happiness, units, by, sitting, next, to, b = line.rstrip('.\n').split()
	n = int(n)
	if verb == 'lose': n = -n
	diff[a][b] = n

print max(Evaluate(p, True)  for p in permutations(diff.keys()))  # Part 1
print max(Evaluate(p, False) for p in permutations(diff.keys()))  # Part 2
