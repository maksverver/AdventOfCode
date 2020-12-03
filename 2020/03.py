from functools import reduce
from operator import mul
import sys

grid = [line.rstrip() for line in sys.stdin]
H = len(grid)
W = len(grid[0])

def CountTrees(right, down):
    trees = 0
    row = 0
    col = 0
    while row < H:
        trees += grid[row][col] == '#'
        row += down
        col += right
        col %= W
    return trees

# Part 1
print(CountTrees(3, 1))

# Part 2
SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(reduce(mul, (CountTrees(r, d) for (r, d) in SLOPES)))
