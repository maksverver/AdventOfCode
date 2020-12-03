import re
import sys

valid = 0
for line in sys.stdin:
    m = re.match('^(\d+)-(\d+) (\w): (\w+)$', line)
    a, b, c, d = m.groups()
    valid += int(a) <= d.count(c) <= int(b)
print(valid)
