from functools import reduce
from math import gcd
import re
import sys

def LeastCommonMultiple(x, y):
    return x * y // gcd(x,y)

def ParseLine(line):
    return tuple(map(int, re.match('<x=(.*), y=(.*), z=(.*)>', line).groups()))

def Update(pv, other_pvs):
    p, v = pv
    v += sum((p < other_p) - (p > other_p) for (other_p, _) in other_pvs)
    p += v
    return (p, v)

def Solve(moons, d):
    '''Solve in dimension `d` only.'''
    # This assumes that the initial state is part of the cycle, which is true
    # (but it's not very obvious).
    initial_pvs = pvs = tuple((moon[d], 0) for moon in moons)
    steps = 0
    while True:
        pvs = tuple(Update(pv, pvs) for pv in pvs)
        steps += 1
        if pvs == initial_pvs:
            return steps

moons = tuple(map(ParseLine, sys.stdin))
print(reduce(LeastCommonMultiple, (Solve(moons, d) for d in range(3))))
