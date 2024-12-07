#!/usr/bin/env python3

from math import floor, log10
from random import randrange, uniform, seed
from functools import cache
import sys

# Limit so that the sum of values still fits in a 48-bit integer
max_val = 2**40

def IntLen(i):
    return 1 if i == 0 else floor(log10(i)) + 1

def IsPossible(target, values):

    for allow_concat in range(2):
        memo = {}
        def Solve(target, n):
            v = values[n := n - 1]
            if n == 0:
                return target == v

            if v == 0 and target == 0:
                return True

            key = len(values) * target + n
            res = memo.get(key)
            if res is None:
                memo[key] = res = (
                    (target >= v and Solve(target - v, n)) or
                    (v != 0 and target % v == 0 and Solve(target // v, n)) or
                    (allow_concat and target % (m := 10**IntLen(v)) == v and Solve(target // m, n)))
            return res

        if Solve(target, len(values)):
            return allow_concat + 1

    return 0


def RandomValue(min_val):
    return randrange(min_val, 10**(randrange(1, 4)))

def Concat(x, y):
    if y == 0:
        return 10*x + y
    return x * 10**IntLen(y) + y


def GenCase(max_terms, min_val):
    allow_concat = randrange(0, 2)
    used_concat = False
    acc = RandomValue(2)
    values = [acc]
    while len(values) < max_terms:
        if min_val <= 1 and uniform(0, 1) < 0.1:
            values.append(1)
            continue

        val = RandomValue(min_val)
        p = uniform(0, 1)
        if p < 0.5:
            if acc + val > max_val:
                break
            acc += val
        elif p < 0.6 or not allow_concat:
            if acc * val > max_val:
                break
            acc *= val
        else:
            if Concat(acc, val) > max_val:
                break
            used_concat = True
            acc = Concat(acc, val)
        values.append(val)

    while min_val <= 0 and len(values) < max_terms // 2:
        _, vals, _ = GenCase(max_terms - len(values) - 1, 1)
        values = vals + [0] + values

    return acc, values, used_concat

def MakeImpossible(target, values):
    while IsPossible(target, values):
        values[randrange(0, len(values))] += 1

def GenCases(output, seed_val, num_cases, max_terms, min_val):
    seed(seed_val)

    answer1 = 0
    answer2 = 0

    cases = []
    for i in range(num_cases):
        target, values, concat = GenCase(max_terms=max_terms, min_val=min_val)
        possible = IsPossible(target, values)
        # if not possible:
        #     print(target, values)
        assert possible > 0
        # Occasionally, it's possible that we generated a case with concat, but it's
        # solvable without concat too, just by random chance.
        assert possible <= concat + 1

        if randrange(0, 3) == 0:
            MakeImpossible(target, values)
        else:    
            answer1 += target * (possible == 1)
            answer2 += target

        cases.append((target, values))
        print(i, target, len(values), values)  # progress

    with open(output + '.txt', 'wt') as f:
        for target, values in cases:
            print(f'{target}:', *values, file=f)

    with open(output + '-output.txt', 'wt') as f:
        print(answer1, file=f)
        print(answer2, file=f)

    print(answer1, file=sys.stderr)
    print(answer2, file=sys.stderr)

GenCases(output='aoc-2024-day-07-challenge-1', seed_val=31337, num_cases=1000, max_terms=13, min_val=2)
GenCases(output='aoc-2024-day-07-challenge-2', seed_val=69420, num_cases=1000, max_terms=40, min_val=1)
GenCases(output='aoc-2024-day-07-challenge-3', seed_val=74747, num_cases=1000, max_terms=100, min_val=0)
