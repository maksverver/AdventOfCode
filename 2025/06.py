from math import prod
import sys

operators = {
    '+': sum,
    '*': prod,
}

# Read grid and split into parts delimited by empty columns:
grid = list(sys.stdin)
cols = [c for c in range(len(grid[0])) if all(row[c].isspace() for row in grid)]
parts = [[row[i+1:j] for row in grid] for i, j in zip([-1] + cols, cols)]

# Now solve each part separately, transposing rows and columns for part 2:
id = lambda x: x
transpose = lambda grid: [''.join(row) for row in zip(*grid)]
for f in id, transpose:
    print(sum(operators[part[-1][0]](map(int, f(part[:-1]))) for part in parts))
