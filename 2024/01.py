import sys

a = []
b = []
for line in sys.stdin:
    x, y = map(int, line.split())
    a.append(x)
    b.append(y)

# Part 1
print(sum(abs(x - y) for x, y in zip(sorted(a), sorted(b))))

# Part 2
print(sum(x * b.count(x) for x in a))
