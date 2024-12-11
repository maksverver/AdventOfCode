from functools import cache
from math import floor, log10
import sys

@cache
def Calc(i, n):
    '''Calculates the number of stones after blinking `n` times,
       if we start with a single stone engraved with `i`.'''

    # No blinks left. We have 1 stone.
    if n == 0:
        return 1

    # If the number is 0, it becomes 1.
    if i == 0:
        return Calc(1, n - 1)

    # If the number of digits is even, the number is split in half.
    digits = floor(log10(i)) + 1
    if digits % 2 == 0:
        div = 10**(digits // 2)
        return Calc(i // div, n - 1) + Calc(i % div, n - 1)

    # Otherwise, the number is multiplied by 2024.
    return Calc(i * 2024, n - 1)


stones = list(map(int, sys.stdin.read().split()))
for n in 25, 75:
    print(sum(Calc(i, n) for i in stones))
