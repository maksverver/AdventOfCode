#!/usr/bin/env python3

from random import randrange, seed

def GenCase(output, seed_val, size):
    seed(seed_val)

    assert size % 2 == 1

    case = ''.join(str(randrange(1 - i%2, 10)) for i in range(size))
    with open(output + '.txt', 'wt') as f:
        print(case, file=f)

GenCase(output='aoc-2024-day-09-challenge-1', seed_val=31337, size=10**5+1)
GenCase(output='aoc-2024-day-09-challenge-2', seed_val=69420, size=10**6+1)
GenCase(output='aoc-2024-day-09-challenge-3', seed_val=74747, size=10**7+1)
GenCase(output='aoc-2024-day-09-challenge-3a', seed_val=74747, size=10**7//2+1)
