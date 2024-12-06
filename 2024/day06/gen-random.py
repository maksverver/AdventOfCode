from random import uniform

W = 999
H = 1999

# Note: this doesn't always generate valid grids!

grid = [['.#'[uniform(0, 1) < 0.02] for _ in range(W)] for _ in range(H)]
grid[H//2][W//2] = '^'
for row in grid:
    print(''.join(row))
