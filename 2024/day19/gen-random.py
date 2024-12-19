from math import *
from random import *
import sys

ALPHABET = 'bgruw'
MAX_LENGTH = 25
MAX_NUM_PER_LENGTH = 20

def GenRandomPattern(length):
    s = ''
    while len(s) < length:
        s += choice(ALPHABET)
    return s

def GenRandomPatterns(length):
    count = min(len(ALPHABET)**length // 2, MAX_NUM_PER_LENGTH)
    s = set()
    while len(s) < count:
        s.add(GenRandomPattern(length))
    return s

patterns = [p for length in range(1, MAX_LENGTH + 1) for p in GenRandomPatterns(length)]

def Solve(target):
    count = [1] + [0]*len(target)
    for i in range(len(target)):
        for s in patterns:
            if target.find(s, i, i + len(s)) == i:
                count[i + len(s)] += count[i]
    return count[len(target)]

def GenPossible(min_len):
    s = ''
    while len(s) < min_len:
        s += choice(patterns)
    return s

def MakeImpossible(s):
    while Solve(s):
        i = randrange(0, len(s))
        s = s[:i] + choice(ALPHABET) + s[i+1:]
    return s

num_possible = 543
total_cases = 1000
cases = (
    [GenPossible(1000) for _ in range(num_possible)] +
    [MakeImpossible(GenPossible(1000)) for _ in range(total_cases - num_possible)])

shuffle(patterns)
print(*patterns, sep=', ')
print()
shuffle(cases)
for case in cases:
    print(case)
