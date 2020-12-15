import sys

nums = [int(s) for s in sys.stdin.readline().split(',')]

def Solve(iterations):
    # Alternative implementation that uses a list instead of a dictionary,
    # which works because the keys are ints between 0 and iterations.
    #
    # Filling the list with 0 instead of None makes the code run faster with
    # PyPy (presumably it uses an int array specialization internally).
    index = iterations*[0]
    for i in range(1, len(nums)):
        index[nums[i - 1]] = i
    i = len(nums)
    n = nums[i - 1]
    while i < iterations:
        k = index[n]
        m = 0 if k == 0 else i - k
        index[n] = i
        i += 1
        n = m
    return n

print(Solve(2020))
print(Solve(30000000))
