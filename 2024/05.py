# Brute force, but correct!

import sys

part1, part2 = sys.stdin.read().strip().split('\n\n')

orders = []
for line in part1.split():
    a, b = map(int, line.split('|'))
    orders.append((a, b))

def FindInvalidPair(pages):
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            if (pages[j], pages[i]) in orders:
                return i, j

answer1 = 0
answer2 = 0
for line in part2.split():
    pages = list(map(int, line.split(',')))
    assert len(pages) % 2 == 1
    already_sorted = True
    while ij := FindInvalidPair(pages):
        # j-th page belongs before i-th page; move it!
        already_sorted = False
        i, j = ij
        pages = pages[:i] + pages[j:j+1] + pages[i:j] + pages[j+1:]
    middle = pages[len(pages) // 2]
    if already_sorted:
        answer1 += middle
    else:
        answer2 += middle
print(answer1)
print(answer2)
