from random import sample

walls = set()
extra = []

r = c = 0

k = 1
while k < 789:
    r -= k
    walls.add((r - 1, c))
    for i in range(1, k + 2): extra.append((r - 1, c + i))
    c += k
    walls.add((r, c + 1))
    k += 2
    for i in range(1, k + 2): extra.append((r + i, c + 1))
    r += k
    walls.add((r + 1, c))
    for i in range(1, k + 2): extra.append((r + 1, c - i))
    c -= k
    walls.add((r, c - 1))
    for i in range(1, k + 2): extra.append((r - i, c - 1))
    k += 2

min_r = min(r for (r, c) in walls)
min_c = min(c for (r, c) in walls)
max_r = max(r for (r, c) in walls)
max_c = max(c for (r, c) in walls)

height = max_r - min_r + 1
width = max_c - min_c + 1

grid = [['.']*width for _ in range(height)]
for (r, c) in walls:
    grid[r - min_r][c - min_c] = '#'
assert grid[-min_r][-min_c] == '.'
grid[-min_r][-min_c] = '^'

for r, c in sample(extra, int(len(extra) * 0.3)):
    assert grid[r - min_r][c - min_c] == '.'
    grid[r - min_r][c - min_c] = '#'

for row in grid:
    print(''.join(row))

# TODO: add extra walls in unused rows/columns 

