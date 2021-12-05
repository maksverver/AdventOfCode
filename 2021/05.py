from collections import Counter
import re
import sys

counter1 = Counter()  # counts points covered by horizontal/vertical lines
counter2 = Counter()  # counts points covered by (anti)diagonal lines
pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
for line in sys.stdin:
    x1, y1, x2, y2 = map(int, pattern.match(line).groups())
    length = max(abs(x2 - x1), abs(y2 - y1))
    dx = (x2 > x1) - (x2 < x1)
    dy = (y2 > y1) - (y2 < y1)
    counter = (counter1 if dx == 0 or dy == 0 else counter2)
    counter.update((x1 + dx * i, y1 + dy * i) for i in range(length + 1))
counter2 += counter1
print(sum(n > 1 for n in counter1.values()))
print(sum(n > 1 for n in counter2.values()))
