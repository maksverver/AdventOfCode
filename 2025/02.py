import sys

ranges = []
for part in sys.stdin.read().strip().split(','):
    lo, hi = map(int, part.split('-'))
    ranges.append((lo, hi))

assert max(hi for (lo, hi) in ranges) <= 10**10

invalid1 = set()
invalid2 = set()
for i in range(1, 10**5):
    s = str(i)
    invalid1.add(int(s*2))
    n = 2
    while n*len(s) <= 10:
        invalid2.add(int(s*n))
        n += 1

print(sum(inv for lo, hi in ranges for inv in invalid1 if lo <= inv <= hi))
print(sum(inv for lo, hi in ranges for inv in invalid2 if lo <= inv <= hi))
