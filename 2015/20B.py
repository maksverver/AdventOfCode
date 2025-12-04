from collections import defaultdict
from itertools import count
import sys

cutoff = int(sys.stdin.read())
elves = defaultdict(list)
for i in count(1):
	elves[i].append(i)
	presents = sum(elves[i])*11
	if presents >= cutoff:
		print(i)
		break
	for j in elves[i]:
		if i + j <= 50*j:
			elves[i + j].append(j)
	del elves[i]
