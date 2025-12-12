import re
import sys

answer = 0
for line in sys.stdin:
    if 'x' in line:
        h, w, *counts = map(int, re.findall(r'\d+', line))
        answer += h*w > 8*sum(counts)
print(answer)
