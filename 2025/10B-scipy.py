# Advent of Code 2025 day 10 (https://adventofcode.com/2025/day/10)
#
# Solution for part 2 using scipy.optimize.linprog

import sys

from scipy.optimize import linprog

def Solve(buttons, joltage):
    matrix = [[i in b for b in buttons] for i in range(len(joltage))]
    res = linprog([1]*len(buttons), A_eq=matrix, b_eq=joltage, integrality=1)
    assert res.success
    return round(sum(res.x))

answer = 0
for line in sys.stdin:
    _lights, *buttons, joltage = line.split()
    buttons = [{int(i) for i in button.strip('()').split(',')} for button in buttons]
    joltage = [int(i) for i in joltage.strip('{}').split(',')]
    answer += Solve(buttons, joltage)
print(answer)
