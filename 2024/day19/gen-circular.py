from math import *
from random import *
import sys

def shuffled(iterable):
    l = list(iterable)
    shuffle(l)
    return l

NUM_PATTERNS = 90
MAX_PATTERN_LENGTH = 500
MIN_CASE_LENGTH = 500
MAX_CASE_LENGTH = 1000
NUM_POSSIBLE = 669  # is answer to part 1
TOTAL_CASES = 1000

ALPHABET = 'bgruw'

def GenRandomPattern(length):
    i = randrange(0, len(ALPHABET))
    return ''.join(ALPHABET[(i + j)%len(ALPHABET)] for j in range(length))

patterns = set()
while len(patterns) < NUM_PATTERNS:
    patterns.add(GenRandomPattern(randint(1, MAX_PATTERN_LENGTH)))

def GenPossible():
    return GenRandomPattern(randint(MIN_CASE_LENGTH, MAX_CASE_LENGTH))

def MakeImpossible(s):
    i = randrange(0, len(s) - 1)
    return s[:i] + s[i+1] + s[i] + s[i+2:]


cases = set()
while len(cases) < NUM_POSSIBLE:
    cases.add(GenPossible())
while len(cases) < TOTAL_CASES:
    cases.add(MakeImpossible(GenPossible()))

print(*shuffled(patterns), sep=', ')
print()
for case in shuffled(cases):
    print(case)
