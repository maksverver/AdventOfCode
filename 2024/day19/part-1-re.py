import re
import sys

a, b = sys.stdin.read().split('\n\n')
patterns = a.split(', ')
targets = b.splitlines()

PAT = re.compile('^(' + '|'.join(patterns) + ')*$')
answer = 0
for target in targets:
    if PAT.match(target):
        answer += 1
print(answer)
