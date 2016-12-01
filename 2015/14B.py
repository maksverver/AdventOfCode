from lib14 import Raindeer
import sys

deer = map(Raindeer, sys.stdin)
points = { d.name: 0 for d in deer }
for t in range(1, 2503 + 1):
	m = max(d.position_at(t) for d in deer)
	for d in deer:
		if d.position_at(t) == m:
			points[d.name] += 1
print max(points.values())
