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
    # Note: this implementation assumes all values are nonnegative.

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

    # Reconstructs the solution expression as a string (or None if the expression
    # is not solvable). The logic here must be kept in sync with Solve() above.
    def DebugString(target, n):
        v = values[n := n - 1]
        if n == 0:
            if target == v:
                return str(v)
            return None
        if v == 0 and target == 0:
            return '+'.join(map(str, values[:n])) + '*0'
        if target >= v and Solve(target - v, n):
            return DebugString(target - v, n) + '+' + str(v)
        if v != 0 and target % v == 0 and Solve(target // v, n):
            return DebugString(target // v, n) + '*' + str(v)
        if part2 and target % (m := 10**IntLen(v)) == v and Solve(target // m, n):
            return DebugString(target // m, n) + '||' + str(v)
        return None

    assert all(v >= 0 for v in values)

    # Uncomment this to debug-print solutions:
    #print(part2, target, DebugString(target, len(values)), file=sys.stderr)

    return Solve(target, len(values))

answer1 = 0
answer2 = 0
for target, values in map(ParseLine, sys.stdin):
    if IsPossible(target, values, 0):
        answer1 += target
    elif IsPossible(target, values, 1):
        answer2 += target
print(answer1)
print(answer2)
