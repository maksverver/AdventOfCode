import sys

M = 20201227

def ModLog(s, y):
    '''Finds exponent `n` such that s**n % M == y in O(n) time.'''
    x = 1
    n = 0
    while x != y:
        x = (x * s) % M
        n += 1
    return n

def ModPow(s, n):
    '''Calculates s**n % M in O(log n) time.'''
    x = 1
    while n > 0:
        if n & 1:
            x = (s * x) % M
        s = (s * s) % M
        n >>= 1
    return x

a, b = map(int, sys.stdin)
print(ModPow(a, ModLog(7, b)))
