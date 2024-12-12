from random import choice, randrange, shuffle, uniform
import sys
from math import *

W = int(sys.argv[1])
H = W * 2 // 3

grid = [['.']*W for _ in range(H)]

# Random BFS
def FillRegion1(r, c, ch, max_size):
    size = 1
    grid[r][c] = ch
    todo = [(r, c)]
    while todo and size < max_size:
        i = randrange(0, len(todo))
        todo[i], todo[-1] = todo[-1], todo[i]
        r, c = todo.pop()
        for r2, c2 in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
            if 0 <= r2 < H and 0 <= c2 < W and grid[r2][c2] != ch:
                size += 1
                grid[r2][c2] = ch
                todo.append((r2, c2))

# Random walk
def FillRegion2(r, c, ch, max_size):
    size = 1
    grid[r][c] = ch
    while size < max_size:
        r2, c2 = choice(((r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)))
        if 0 <= r2 < H and 0 <= c2 < W:
            r, c = r2, c2
            if grid[r2][c2] != ch:
                size += 1
                grid[r2][c2] = ch

def shuffled(s):
    res = list(s)
    shuffle(res)
    return res

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

positions = [(r, c) for r in range(H) for c in range(W)]
shuffle(positions)
total_size = H * W
regions = 1000
sizes = [e**uniform(1, log(total_size)) for _ in range(regions)]
sizes.sort(reverse=True)
for i, (r, c) in enumerate(positions[:regions]):
    size = sizes[i]
    f = [FillRegion1, FillRegion2][size < total_size*0.1 and i % 2]
    f(r, c, chars[i % len(chars)], size)
    print('%.2f%% done' % (100.0 * i // regions,), file=sys.stderr)

assert(grid[r][c] != '.' for r in range(H) for c in range(W))

for row in grid:
    print(''.join(row))

# for target in chars:
#     print()
#     for row in grid:
#         print(''.join('.#'[ch == target] for ch in row))
