from collections import defaultdict
from itertools import count
import sys

cutoff = int(sys.stdin.read())
elves = defaultdict(list)
for i in count(1):
	elves[i].append(i)
	presents = sum(elves[i])*10
	if presents >= cutoff:
		break
	for j in elves[i]:
		elves[i + j].append(j)
	del elves[i]
print i
