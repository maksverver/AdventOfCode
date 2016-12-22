import re
import sys

nodes = []
for line in sys.stdin:
  m = re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T', line)
  if m:
    x, y, size, used, avail = map(int, m.groups())
    nodes.append((used, avail))

print sum(i != j and 0 < a_used <= b_avail
    for i, (a_used, _) in enumerate(nodes)
    for j, (_, b_avail) in enumerate(nodes))
