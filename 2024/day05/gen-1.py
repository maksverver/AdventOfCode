# Generates cases where we have 10 pages ordered 0 < 1 < .. < 8 < 9
#
# Cases are of two forms:
#
#  1. odd-length subarrays in order, e.g. 0,1,2,3,4 or 7,8,9
#  2. odd-length subarrays shuffled, e.g. 4,2,1,3,0 or 7,9,8
#
# These are all well-ordered but can not be sorted with an O(N log N)
# routine without first calculating the transitive closure of elements!

from random import shuffle, randint, sample
import sys

order = [(i - 1, i) for i in range(1, 10)]

answer1 = []
answer2 = []
cases = []
for c in range(100):
    i = randint(0, 7)
    k = randint(1, (9 - i)//2)
    j = i + 1 + 2*k
    case = list(range(i, j))
    assert j <= 10
    if c % 2 == 0:
        assert case[k] == sorted(case)[k]
        answer1.append(case[k])
    else:
        answer2.append(case[k])
        while case[k] == sorted(case)[k]:
            shuffle(case)
    cases.append(case)

shuffle(order)
shuffle(cases)

# remap pages from 0..9 to random numbers between 10 and 99 inclusive
page_mapping = sample(range(10, 100), 10)

for p, q in order:
    print('%d|%d' % (page_mapping[p], page_mapping[q]))
print()
for case in cases:
    print(','.join(str(page_mapping[p]) for p in case))

print(sum(page_mapping[p] for p in answer1), file=sys.stderr)
print(sum(page_mapping[p] for p in answer2), file=sys.stderr)
