from random import choices, randrange

H = 101
W = 101

grid = [[choices(population='.#', weights=[3,1])[0] for _ in range(W)] for _ in range(H)]
grid[randrange(0, H)][randrange(0, W)] = 'S'
for r in range(H): grid[r][0] = grid[r][W - 1] = '.'
for c in range(W): grid[0][c] = grid[H - 1][c] = '.'
for row in grid:
  print(''.join(row))
