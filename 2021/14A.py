from collections import Counter
import sys

template, rules = sys.stdin.read().rstrip().split('\n\n')

rules = dict((rule.split(' -> ') for rule in rules.split('\n')))

def Step(s):
    t = ''
    for i, c in enumerate(s):
        insert = i > 0 and rules.get(s[i - 1: i + 1])
        if insert:
            t += insert
        t += c
    return t

s = template
for _ in range(10):
    s = Step(s)
counts = [v for (k, v) in Counter(s).items()]
print(max(counts) - min(counts))
