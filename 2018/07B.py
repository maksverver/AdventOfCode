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

time = 0
workers = 5
working = []
executed = []
enabled = [x for x in rdeps if not deps[x]]
heapify(enabled)
while True:
    if workers and enabled:
        workers -= 1
        x = heappop(enabled)
        duration = ord(x) - ord('A') + 61
        heappush(working, (time + duration, x))
    elif working:
        time, x = heappop(working)
        executed.append(x)
        for y in rdeps[x]:
            deps[y].remove(x)
            if not deps[y]:
                heappush(enabled, y)
        workers += 1
    else:
        break
print(time)
