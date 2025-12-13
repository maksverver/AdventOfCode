# Advent of Code 2025 day 10 (https://adventofcode.com/2025/day/10)
#
# Solution based on this reddit post:
# https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
#
# For part 2: in any solution, there is a subset of buttons that were pressed an
# odd number of times. The sum of the outputs of these buttons must be odd in
# exactly the same columns where the total joltage levels are odd. So we can
# build a recursive solution: for any set of buttons that makes the joltage
# levels even, we can subtract the effect of these buttons, divide joltage
# levels by half, and solve recursively.

from collections import defaultdict
from math import inf
import sys

# Given a list of buttons (where each button is a set of indices of affected
# lights), returns a dictionary that maps a frozenset of lights to toggle to
# a list of frozensets of buttons that would toggle those lights when pressed.
def CombinePresses(buttons):
    result = defaultdict(list)
    def Go(i, pressed, toggled):
        if i == len(buttons):
            result[toggled].append(pressed)
            return
        Go(i + 1, pressed, toggled)
        Go(i + 1, pressed | {buttons[i]}, toggled ^ buttons[i])
    Go(0, frozenset(), frozenset())
    return result

answer1 = 0
answer2 = 0

for line in sys.stdin:
    lights, *buttons, joltage = line.split()
    lights = frozenset(i for i, ch in enumerate(lights.strip('[]')) if ch == '#')
    buttons = [frozenset(int(i) for i in button.strip('()').split(',')) for button in buttons]
    joltage = [int(i) for i in joltage.strip('{}').split(',')]

    # frozenset of lights to toggle -> list of set of buttons to press
    toggling = CombinePresses(buttons)

    def SolveRecursive(joltage):
        if any(j < 0 for j in joltage):
            return inf

        if all(j == 0 for j in joltage):
            return 0

        odd_indices = frozenset(i for i, j in enumerate(joltage) if j % 2 == 1)

        answer = inf
        for pressed in toggling[odd_indices]:
            new_joltage = list(joltage)
            for button in pressed:
                for i in button:
                    new_joltage[i] -= 1
            for i in range(len(new_joltage)):
                assert new_joltage[i] % 2 == 0
                new_joltage[i] //= 2
            answer = min(answer, len(pressed) + 2*SolveRecursive(new_joltage))
        return answer

    answer1 += min(map(len, toggling[lights]))
    answer2 += SolveRecursive(joltage)

print(answer1)
print(answer2)
