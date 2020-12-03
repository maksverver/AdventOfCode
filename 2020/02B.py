import re
import sys

valid = 0
for line in sys.stdin:
    m = re.match('^(\d+)-(\d+) (\w): (\w+)$', line)
    a, b, c, d = m.groups()
    valid += (d[int(a) - 1] == c) != (d[int(b) - 1] == c)
print(valid)
