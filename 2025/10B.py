# Advent of Code 2025 day 10 (https://adventofcode.com/2025/day/10)
#
# Solution for part 2, using Gauss-Jordan elimination to find free variables,
# and then brute force all possible assignments.

import sys

from itertools import product
from fractions import Fraction
from math import inf

# Performs Gauss-Jordan elimination on the first (n-1) columns of the m x n
# augmented matrix.
#
# Returns a list of column indices corresponding to free variables.
#
def GaussJordan(a):
    m = len(a)
    n = len(a[0])
    free = []
    row = 0
    for col in range(n - 1):
        # Find a row with `col` as the leading nonzero column
        r = row
        while r < m and not a[r][col]:
            r += 1
        if r == m:
            free.append(col)
            continue

        # Move that row towards the top
        a[r], a[row] = a[row], a[r]

        # Normalize row so the leading value is 1
        for c in range(n):
            if c != col:
                a[row][c] /= a[row][col]
        a[row][col] = 1

        # Clear the rest of the column
        for r in range(m):
            if r != row and a[r][col]:
                x = a[r][col] / a[row][col]
                for c in range(n):
                    a[r][c] -= a[row][c] * x

        row += 1

    return free


def Solve(buttons, joltage):
    # Create an augmented matrix of size m x (n + 1) where m is the number of
    # joltages and n is the number of buttons.
    augmented = [
        [Fraction(i in buttons[j]) for j in range(len(buttons))] + [joltage[i]]
        for i in range(len(joltage))]

    free = GaussJordan(augmented)
    bounds = [range(min(joltage[i] for i in buttons[j]) + 1) for j in free]

    best_answer = inf
    for assigned in product(*bounds):
        answer = sum(assigned)
        for row in augmented:
            val = row[-1] - sum(k*row[c] for c, k in zip(free, assigned))
            if val.numerator < 0 or val.denominator != 1:
                break
            answer += val
        else:
            best_answer = min(answer, best_answer)
    return best_answer


answer = 0
for line in sys.stdin:
    _lights, *buttons, joltage = line.split()
    buttons = [{int(i) for i in button.strip('()').split(',')} for button in buttons]
    joltage = [int(i) for i in joltage.strip('{}').split(',')]
    answer += Solve(buttons, joltage)
print(answer)
