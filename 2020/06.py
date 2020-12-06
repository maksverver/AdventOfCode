import sys

groups = [[set(l) for l in g.split()] for g in sys.stdin.read().split('\n\n')]

print(sum(len(set.union(*g)) for g in groups))
print(sum(len(set.intersection(*g)) for g in groups))
