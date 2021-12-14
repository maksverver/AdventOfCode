from collections import Counter
from memoize import Memoize
import sys

template, rules = sys.stdin.read().rstrip().split('\n\n')
rules = dict((rule.split(' -> ') for rule in rules.split('\n')))

@Memoize
def Calc(a, b, n):
    if n == 0:
        return Counter()
    insert = rules[a + b]
    if insert is None:
        return Counter()
    return Counter(insert) + Calc(a, insert, n - 1) + Calc(insert, b, n - 1)

def Solve(n):
    c = Counter(template)
    for i in range(len(template) - 1):
        c += Calc(template[i], template[i + 1], n)
    counts = [v for (k, v) in c.items()]
    return max(counts) - min(counts)

print(Solve(10))
print(Solve(40))
