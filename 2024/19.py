from functools import cache
import sys

a, b = sys.stdin.read().split('\n\n')
patterns = a.split(', ')
targets = b.splitlines()

def Calc(target):
    @cache
    def Search(pos):
        if pos == len(target):
            return 1
        return sum(Search(pos + len(s)) for s in patterns
            if target.find(s, pos, pos + len(s)) == pos)
    return Search(0)

answer1 = 0
answer2 = 0
for target in targets:
    n = Calc(target)
    answer1 += n > 0
    answer2 += n
print(answer1)
print(answer2)
