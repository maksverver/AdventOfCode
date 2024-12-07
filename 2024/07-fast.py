from math import floor, log
from operator import add, mul
import sys

def ParseLine(line):
    target, values = line.split(': ')
    return int(target), tuple(map(int, values.split()))

def IntLen(i):
    '''Returns the number of digits in the decimal representation of i.'''
    return floor(log(i, 10)) + 1

def IsPossible(target, values, part2):
    # Calculates whether it is possible to construct target value `target` using
    # the first `n` elements
    #
    # Essentially this works back from the end of the array to see if the target
    # value can be constructed using the given operands, while the slower
    # implementation in 07.py works from the front to construct all possible
    # expression values.
    #
    # Note: this implementation assumes all values are positive.
    def Solve(target, n):
        v = values[n := n - 1]
        if n == 0:
            return target == v

        return (
            (target > v and Solve(target - v, n)) or
            (target % v == 0 and Solve(target // v, n)) or
            (part2 and target % (m := 10**IntLen(v)) == v and Solve(target // m, n)))

    assert(v > 0 for v in values)

    return Solve(target, len(values))

def Solve(cases, part2):
    return sum(target for target, values in cases if IsPossible(target, values, part2))

cases = list(map(ParseLine, sys.stdin))
print(Solve(cases, False))
print(Solve(cases, True))
