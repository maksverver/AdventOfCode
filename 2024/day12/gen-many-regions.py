# Fills a grid randomly with characters drawn from a small set.
#
# This produces many small regions, while still having quite a few
# nontrivial regions.

from random import choice
from math import *
import sys

W = int(sys.argv[1])
H = round(W * 1.5)

letters = 'FOOBBBAAAARRRRRR'

grid = [[choice(letters) for c in range(W)] for r in range(H)]

for row in grid:
    print(''.join(row))

# print()
# for row in grid:
#     print(''.join('.#'[ch == 'F'] for ch in row))
# print()
# for row in grid:
#     print(''.join('.#'[ch == 'O'] for ch in row))
# print()
# for row in grid:
#     print(''.join('.#'[ch == 'B'] for ch in row))
# print()
# for row in grid:
#     print(''.join('.#'[ch == 'A'] for ch in row))
# print()
# for row in grid:
#     print(''.join('.#'[ch == 'R'] for ch in row))
