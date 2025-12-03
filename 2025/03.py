from math import inf
from functools import cache
import sys

def Solve(row, k):
    @cache
    def MaxVal(n, k):
        '''Best way to take k digits from the first n digits of row'''
        if k == 0: return 0
        if n < k: return -inf
        return max(10*MaxVal(n - 1, k - 1) + row[n - 1], MaxVal(n - 1, k))
    return MaxVal(len(row), k)

grid = [list(map(int, line.strip())) for line in sys.stdin]

for k in (2, 12):
    print(sum(Solve(row, k) for row in grid))
