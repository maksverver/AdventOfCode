from collections import Counter
from math import floor, log10
import sys

def Next(i):
    if i == 0:
        yield 1
    elif (digits := floor(log10(i)) + 1) % 2 == 0:
        div = 10**(digits // 2)
        yield i // div
        yield i % div
    else:
        yield i * 2024

def Step(counter):
    c = Counter()
    for i, n in counter.items():
        for j in Next(i):
            c[j] += n
    return c

def Solve(counter, steps):
    for _ in range(steps):
        counter = Step(counter)
    return counter

stones = Counter(list(map(int, sys.stdin.read().split())))
for steps in 25, 75:
    print(sum(Solve(stones, steps).values()))
