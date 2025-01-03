from math import floor, log10
from operator import add, mul
import sys

def ParseLine(line):
    target, values = line.split(': ')
    return int(target), tuple(map(int, values.split()))

def IsPossible(ops, target, values):
    def calc(acc, pos):
        if pos == len(values):
            return acc == target
        return any(calc(op(acc, values[pos]), pos + 1) for op in ops)
    return calc(values[0], 1)

def Solve(cases, ops):
    return sum(target for target, values in cases if IsPossible(ops, target, values))

def cat(x, y):
    if y == 0: return 10*x                    # not needed for official data
    #return int(str(x) + str(y))              # straightforward implementation
    return 10**(floor(log10(y)) + 1) * x + y  # slightly faster implementation

cases = list(map(ParseLine, sys.stdin))
print(Solve(cases, [add, mul]))
print(Solve(cases, [add, mul, cat]))
