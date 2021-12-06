from collections import Counter
import sys

c = Counter(map(int, sys.stdin.readline().split(',')))

def Step(c):
    d = Counter()
    for k, v in c.items():
        if k > 0:
            d[k - 1] += v
        else:
            d[6] += v
            d[8] += v
    return d

# Part 1
for _ in range(80):
    c = Step(c)
print(sum(c.values()))

# Part 2
for _ in range(80, 256):
    c = Step(c)
print(sum(c.values()))
