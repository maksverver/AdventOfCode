# Advent of Code 2025 day 10 (https://adventofcode.com/2025/day/10)
#
# Solution for part 1 only, using breadth-first search to find the
# smallest subset of buttons to press to toggle the required lights.

import sys

def Solve(lights, buttons):
    dist = {0: 0}
    todo = [0]
    for have in todo:
        for mask in buttons:
            next = have ^ mask
            if next not in dist:
                dist[next] = dist[have] + 1
                todo.append(next)
                if next == lights:
                    return dist[lights]
    # No solution found! (Shouldn't happen.)
    assert False

answer = 0
for line in sys.stdin:
    lights, *buttons, _joltage = line.split()
    lights = sum(2**i for i, ch in enumerate(lights.strip('[]')) if ch == '#')
    buttons = [sum(2**int(i) for i in button.strip('()').split(',')) for button in buttons]
    answer += Solve(lights, buttons)
print(answer)
