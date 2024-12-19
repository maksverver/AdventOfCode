import sys

a, b = sys.stdin.read().split('\n\n')
patterns = a.split(', ')
targets = b.splitlines()

def Calc(target):
    count = [1] + [0]*len(target)
    for i in range(len(target)):
        for s in patterns:
            if target.find(s, i, i + len(s)) == i:
                count[i + len(s)] += count[i]
    return count[len(target)]

answer1 = 0
answer2 = 0
for target in targets:
    n = Calc(target)
    answer1 += n > 0
    answer2 += n
print(answer1)
print(answer2)
