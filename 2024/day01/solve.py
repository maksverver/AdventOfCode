from collections import Counter
import sys
from time import time

t1 = time()

a = []
b = []
for line in sys.stdin:
    x, y = map(int, line.split())
    a.append(x)
    b.append(y)

t2 = time()

# Part 1
print(sum(abs(x - y) for x, y in zip(sorted(a), sorted(b))))

t3 = time()

# Part 2
ac = Counter(a)
bc = Counter(b)
print(sum(n * x * bc[x] for (x, n) in ac.items()))

t4 = time()

print('Input time:  %.3f s' % (t2 - t1), file=sys.stderr)
print('Part 1 time: %.3f s' % (t3 - t2), file=sys.stderr)
print('Part 2 time: %.3f s' % (t4 - t3), file=sys.stderr)
print('Total time:  %.3f s' % (t4 - t1), file=sys.stderr)
