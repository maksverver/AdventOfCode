from intcode import RunMachine
import sys

ints = list(map(int, sys.stdin.readline().split(',')))

blocks = {}
x = y = None
for i in RunMachine(ints, []):
    if x is None:
        x = i
    elif y is None:
        y = i
    else:
        blocks[x, y] = i
        x = y = None
print(sum(v == 2 for v in blocks.values()))
