from math import floor, log
from operator import add, mul
import sys

def ParseLine(line):
    target, values = line.split(': ')
    return int(target), tuple(map(int, values.split()))

def IsPossible(ops, target, values):
    all_positive = all(value > 0 for value in values)
    memo = {}
    def calc(acc, pos):
        if pos == len(values):
            return acc == target
        if all_positive and acc > target:
            return False
        key = (acc, pos)
        res = memo.get(key)
        if res is None:
            memo[key] = res = any(calc(op(acc, values[pos]), pos + 1) for op in ops)
        return res
    return calc(values[0], 1)

def Solve(cases, ops):
    return sum(target for target, values in cases if IsPossible(ops, target, values))

def cat(x, y):
    '''Concatenation operator'''
    #return int(str(x) + str(y))                # straightforward implementation
    return 10**(floor(log(y, 10)) + 1) * x + y  # slightly faster implementation

cases = list(map(ParseLine, sys.stdin))
print(Solve(cases, [add, mul]))
print(Solve(cases, [add, mul, cat]))
