# Generates cases where we have page numbers 10 to 99 inclusive,
# and page numbers are ordered based on the first digit only,
# so not totally ordered.
#
# Generates two kinds of cases:
#
#  1. pick the middle element from the group of 20s, 30s, .., 80s,
#     and add an equal number of random elements from the decimal groups below,
#     keep them in sorted order, e.g.:   11 10 20 22 21 42 55 66 77 88 99
#     (these are already considered sorted and contribute to answer 1)
#  2. the same as above, but now we shuffle the numbers.
#     (these require sorting)
#
# In both cases the middle element is uniquely determined.

from random import shuffle, randint, sample
import sys

order = [(10*k + i, 10*(k + 1) + j) for k in range(1, 9) for i in range(10) for j in range(10)]

sort_key = lambda i: i // 10

answer1 = []
answer2 = []
cases = []
for c in range(100):
    middle_digit = randint(2, 8)
    middle = randint(10*middle_digit, 10*middle_digit + 9)

    lower_remaining = []
    higher_remaining = []

    lower = []
    higher = []
    for d in range(1, 10):
        if d < middle_digit:
            x = randint(10*d, 10*d + 9)
            lower.append(x)
            for y in range(10*d, 10*d + 10):
                if y != x:
                    lower_remaining.append(y)
        if d > middle_digit:
            x = randint(10*d, 10*d + 9)
            higher.append(x)
            for y in range(10*d, 10*d + 10):
                if y != x:
                    higher_remaining.append(y)

    num_extra = randint(
        max(len(lower), len(higher)),
        min(20, len(lower) + len(lower_remaining), len(higher) + len(higher_remaining)))

    shuffle(lower_remaining)
    while len(lower) < num_extra: lower.append(lower_remaining.pop())
    shuffle(higher_remaining)
    while len(higher) < num_extra: higher.append(higher_remaining.pop())
    assert len(lower) == len(higher) == num_extra

    shuffle(lower)
    shuffle(higher)

    if c % 2 == 0:
        lower.sort(key=sort_key)
        higher.sort(key=sort_key)
        cases.append(lower + [middle] + higher)
        answer1.append(middle)
    else:
        case = lower + [middle] + higher
        shuffle(case)
        while case[num_extra] == middle:
            shuffle(case)
        cases.append(case)
        answer2.append(middle)

shuffle(order)
shuffle(cases)

# remap pages from 0..9 to random numbers between 10 and 99 inclusive
# page_mapping = list(range(100))  # no remapping
page_mapping = [None]*10 + sample(range(10, 100), 90)

for p, q in order:
    print('%d|%d' % (page_mapping[p], page_mapping[q]))
print()
for case in cases:
    print(','.join(str(page_mapping[p]) for p in case))

print(sum(page_mapping[p] for p in answer1), file=sys.stderr)
print(sum(page_mapping[p] for p in answer2), file=sys.stderr)
