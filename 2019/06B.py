from collections import defaultdict
import sys

parent = {}
depth = {}
orbiters = defaultdict(list)
for line in sys.stdin:
    a, b = line.strip().split(')')
    orbiters[a].append(b)
    assert b not in parent
    parent[b] = a

def ComputeDepths(a, d):
    depth[a] = d
    for b in orbiters[a]:
        ComputeDepths(b, d + 1)

def FindShortestPath(a, b):
    steps = 0
    while a != b:
        if depth[a] > depth[b]:
            a = parent[a]
        else:
            b = parent[b]
        steps += 1
    return steps

ComputeDepths('COM', 0)
print(FindShortestPath('YOU', 'SAN') - 2)
