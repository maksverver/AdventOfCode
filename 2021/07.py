from math import floor, ceil
import sys

xs = sorted(map(int, sys.stdin.readline().split(',')))

# Part 1: optimal solution is the median value
xx = xs[len(xs) // 2]
print(sum(abs(x - xx) for x in xs))

# Part 2: optimal solution is the mean value (rounded up or down)
# Partial proof: http://www.jerrydallal.com/lhsp/ssq.htm
def Cost(d):
    return abs(d) * (abs(d) + 1) // 2

def Eval(xx):
    return sum(Cost(x - xx) for x in xs)

mean = sum(xs) / len(xs)
print(min(Eval(xx) for xx in [floor(mean), ceil(mean)]))
