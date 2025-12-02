from math import *
from random import randint, uniform

def Generate(k=1000, max_n=10**6):
    scale = log(max_n)
    def GenerateOne():
        x = uniform(0, 1)
        y = uniform(0, 1)
        if x > y:
            x, y = y, x
        lo = floor(exp(scale*x))
        hi = ceil(exp(scale*y))
        assert 1 <= lo <= hi <= max_n
        return lo, hi
    cases = [GenerateOne() for _ in range(k)]
    return ','.join(f'{lo}-{hi}' for (lo, hi) in cases)

if 1:
    with open('challenge-1.txt', 'wt') as f:
        f.write(Generate(10000, 10**6) + '\n')
    with open('challenge-2.txt', 'wt') as f:
        f.write(Generate(10000, 10**9) + '\n')
    with open('challenge-3.txt', 'wt') as f:
        f.write(Generate(10000, 10**12) + '\n')
    with open('challenge-4.txt', 'wt') as f:
        f.write(Generate(10000, 10**15) + '\n')
    with open('challenge-5.txt', 'wt') as f:
        f.write(Generate(10000, 10**17) + '\n')
    with open('challenge-6.txt', 'wt') as f:
        f.write(Generate(10000, 10**18) + '\n')
