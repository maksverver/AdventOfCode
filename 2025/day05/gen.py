#!/usr/bin/env python3

import sys
from random import randint, sample, shuffle

LIM = 10**15

def Covered(ranges):
    i = 0
    total = 0
    missing = []
    for l, r in sorted(ranges):
        if i < l:
            missing.append((i, l))
            i = l
        if i < r:
            total += r - i
            i = r
    if i < LIM:
        missing.append((i, LIM))
    return total, missing


SEGMENTS = 10000
OVERLAP = 20
INGREDIENTS = 100000

points = [0] + sorted(sample(range(1, LIM), k=2*SEGMENTS)) + [LIM]
ranges = []
for i in range(SEGMENTS):
    l = points[2*i+1]
    r = points[2*i+2]
    ranges.append((l, r))
    subpoints = [l] + sorted(sample(range(l + 1, r), OVERLAP)) + [r]
    for _ in range(randint(0, OVERLAP)):
        ranges.append(tuple(sorted(sample(subpoints, k=2))))

included, negative_ranges = Covered(ranges)
excluded = sum(r - l for (l, r) in negative_ranges)
assert included + excluded == LIM

print('overlap', sum(r - l for (l, r) in ranges) / included, file=sys.stderr)
print('included', included, file=sys.stderr)
print('excluded', excluded, file=sys.stderr)
print('len(ranges)         ', len(ranges), file=sys.stderr)
print('len(negative_ranges)', len(negative_ranges), file=sys.stderr)

ingredients = []
for p in points:
    if randint(0, 1) == 0:
        ingredients.append(p)
    if p > 0 and randint(0, 100) == 0:
        ingredients.append(p - 1)
    if p < LIM and randint(0, 100) == 0:
        ingredients.append(p + 1)
while len(ingredients) < INGREDIENTS:
    ingredients.append(randint(0, LIM))

shuffle(ranges)
shuffle(ingredients)
for l, r in ranges:
    print(f'{l}-{r}')
print()
for i in ingredients:
    print(i)
