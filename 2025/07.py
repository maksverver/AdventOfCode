from collections import defaultdict
import sys

start_c = next(sys.stdin).index('S')

answer1 = 0
cs = {start_c: 1}   # column -> number of ways to reach this column
for row in sys.stdin:
    new_cs = defaultdict(int)
    for c, n in cs.items():
        if row[c] == '.':
            new_cs[c] += n
        else:
            assert row[c] == '^'
            new_cs[c - 1] += n
            new_cs[c + 1] += n
            answer1 += 1
    cs = new_cs
answer2 = sum(cs.values())

print(answer1)
print(answer2)
