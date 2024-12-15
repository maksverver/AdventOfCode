# Advent of Code 2024 Day 15: Warehouse Woes
# https://adventofcode.com/2024/day/15

import sys

dirs = {
    '^': (-1,  0),
    'v': (+1,  0),
    '>': ( 0, +1),
    '<': ( 0, -1),
}

grid_data, moves_data = sys.stdin.read().strip().split('\n\n')
moves = ''.join(moves_data.split())
grid1 = [list(row) for row in grid_data.split()]

expand = {
    '.': '..',
    '@': '@.',
    'O': '[]',
    '#': '##',
}

grid2 = [[ch2 for ch in row for ch2 in expand[ch]] for row in grid1]


def PushHorizontal(r, c1, dc):
    c2 = c1
    while grid[r][c2] in 'O[]':
        c2 += dc
    if grid[r][c2] == '#':
        return False
    if dc > 0: grid[r][c1+1:c2+1] = grid[r][c1:c2]
    if dc < 0: grid[r][c2:c1] = grid[r][c2+1:c1+1]
    grid[r][c1] = '.'
    c = c1
    return True


def PushVertical(r, c, dr):
    todo = []
    seen = set()

    def MoveBox(r, c):
        ch = grid[r][c]
        if (r, c) not in seen:
            seen.add((r, c))
            todo.append((r, c))
            if ch == '[': MoveBox(r, c + 1)
            if ch == ']': MoveBox(r, c - 1)

    # Find all blocks that must move, recursively.
    MoveBox(r, c)
    for r, c in todo:
        r += dr
        ch = grid[r][c]
        if ch == '#':
            return False
        if ch in 'O[]':
            MoveBox(r, c)

    # Move blocks in reverse order.
    for r, c in reversed(todo):
        grid[r + dr][c] = grid[r][c]
        grid[r][c] = '.'

    return True


for grid in grid1, grid2:
    (r, c), = ((r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '@')
    grid[r][c] = '.'

    for move in moves:
        dr, dc = dirs[move]
        r1 = r + dr
        c1 = c + dc
        if grid[r1][c1] == '.':
            r, c = r1, c1
        elif grid[r1][c1] != '#':
            if dr == 0 and PushHorizontal(r1, c1, dc):
                c = c1
            elif dc == 0 and PushVertical(r1, c1, dr):
                r = r1

    print(sum(100*r + c
            for r, row in enumerate(grid)
            for c, ch in enumerate(row)
            if ch in '[O'))
