import sys

nums = [int(s) for s in sys.stdin.readline().split(',')]

def Solve(iterations):
    index = dict((n, i) for (i, n) in enumerate(nums[:-1]))
    i = len(nums) - 1
    n = nums[i]
    while i < iterations:
        m = i - index.get(n, i)
        index[n] = i
        i += 1
        n = m
    return n

print(Solve(2020 - 1))
print(Solve(30000000 - 1))
