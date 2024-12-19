from math import *
from random import *
import sys

def shuffled(iterable):
    l = list(iterable)
    shuffle(l)
    return l

# answer2 = factorial(floor(K / 2)) * NUM_POSSIBLE

K = 12
NUM_POSSIBLE = 678  # is answer to part 1
TOTAL_CASES = 1000

patterns = ['uw' * (2**(K + 1) + 2**i) for i in range(K)]

def GenPossible():
    return 'uw' * sum(2**(K + 1) + 2**i for i in sample(range(K), k=K//2))

def GenImpossible():
    return 'uw' * (sum(2**(K + 1) + 2**i for i in sample(range(K), k=K//2)) + 2**K)

cases = set()
while len(cases) < NUM_POSSIBLE:
    cases.add(GenPossible())
while len(cases) < TOTAL_CASES:
    cases.add(GenImpossible())

print(*shuffled(patterns), sep=', ')
print()
for case in shuffled(cases):
    print(case)
