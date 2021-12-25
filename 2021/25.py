import sys

grid = [list(line.rstrip()) for line in sys.stdin]
H = len(grid)
W = len(grid[0])

def MoveRight(old_grid):
    new_grid = list(map(list, old_grid))
    for r in range(H):
        for c in range(W):
            if old_grid[r][c - 1] == '>' and old_grid[r][c] == '.':
                new_grid[r][c - 1] = '.'
                new_grid[r][c] = '>'
    return new_grid

def MoveDown(old_grid):
    new_grid = list(map(list, old_grid))
    for r in range(H):
        for c in range(W):
            if old_grid[r - 1][c] == 'v' and old_grid[r][c] == '.':
                new_grid[r - 1][c] = '.'
                new_grid[r][c] = 'v'
    return new_grid

def Move(grid):
    grid = MoveRight(grid)
    grid = MoveDown(grid)
    return grid

def Key(grid):
    return '\n'.join(map(''.join, grid))

seen = set()
key = Key(grid)
while key not in seen:
    seen.add(key)
    grid = Move(grid)
    key = Key(grid)
print(len(seen))
