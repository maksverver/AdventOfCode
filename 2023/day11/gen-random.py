from random import choices, random, randint

# H, W = 320, 240     # small
# H, W = 1440, 1024   # medium
H, W = 6000, 4000   # large

p_galaxy    = 0.2
p_empty_row = 0.3
p_empty_col = 0.3

grid = [['.#'[random() < p_galaxy] for _ in range(W)] for _ in range(H)]

for r in choices(range(H), k=int(H*p_empty_row)):
  for c in range(W):
    grid[r][c] = '.'

for c in choices(range(W), k=int(W*p_empty_row)):
  for r in range(H):
    grid[r][c] = '.'

for row in grid:
  print(''.join(row))

#print(sum(grid[r][c] == '#' for r in range(H) for c in range(W)))
