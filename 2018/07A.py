from collections import defaultdict
from heapq import heapify, heappush, heappop
import re
import sys

deps = defaultdict(set)
rdeps = defaultdict(set)
for line in sys.stdin:
    a, b = re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', line).groups()
    deps[b].add(a)
    rdeps[a].add(b)

executed = []
enabled = [x for x in rdeps if not deps[x]]
heapify(enabled)
while enabled:
    x = heappop(enabled)
    executed.append(x)
    for y in rdeps[x]:
        deps[y].remove(x)
        if not deps[y]:
            heappush(enabled, y)
print(''.join(executed))
