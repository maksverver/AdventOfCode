from math import floor, log10
from operator import add, mul
import sys

def ParseLine(line):
    target, values = line.split(': ')
    return int(target), tuple(map(int, values.split()))

def IntLen(i):
    '''Returns the number of digits in the decimal representation of i.'''
    return 1 if i == 0 else floor(log10(i)) + 1

def IsPossible(target, values, part2):
    # Calculates whether it is possible to construct target value `target` using
    # exactly the first `n` elements of `values`.
    #
    # Compared to 07.py, which recursively constructs all results from front to
    # back, this essentially runs from back to front, determining only if it is
    # possible to construct the desired target.
    #
    # To construct x from [a_1, a_2, .. a_n] we need to be able to:
    #
    #   construct (x - a_n) from [a_1, a_2, .. a_(n-1)], or
    #   construct (x / a_n) from [a_1, a_2, .. a_(n-1)], or
    #   construct (x without suffix a_n) from [a_1, a_2, .. a_(n-1)] (part 2 only)
    #
    # Note: this implementation assumes all values are positive.

    memo = {}
    def Solve(target, n):
        v = values[n := n - 1]
        if n == 0:
            return target == v

        if v == 0 and target == 0:
            return True

        key = len(values)*target + n
        res = memo.get(key)
        if res is None:
            memo[key] = res = (
                (target >= v and Solve(target - v, n)) or
                (v != 0 and target % v == 0 and Solve(target // v, n)) or
                (part2 and target % (m := 10**IntLen(v)) == v and Solve(target // m, n)))
        return res

    assert(v > 0 for v in values)

    return Solve(target, len(values))

def Solve(cases, part2):
    return sum(target for target, values in cases if IsPossible(target, values, part2))

cases = list(map(ParseLine, sys.stdin))
print(Solve(cases, False))
print(Solve(cases, True))
