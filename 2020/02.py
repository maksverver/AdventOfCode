import re
import sys

valid1 = valid2 = 0
for line in sys.stdin:
    m = re.match('^(\d+)-(\d+) (\w): (\w+)$', line)
    a, b, c, d = m.groups()
    valid1 += int(a) <= d.count(c) <= int(b)
    valid2 += (d[int(a) - 1] == c) != (d[int(b) - 1] == c)
print(valid1)
print(valid2)
