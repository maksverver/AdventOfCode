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
original_grid = [list(row) for row in grid_data.split()]


def CoordinateSum(grid, box_char):
    return sum(100*r + c
            for r, row in enumerate(grid)
            for c, ch in enumerate(row)
            if ch == box_char)


def Part1():
    # Make a working copy of the grid.
    grid = [list(row) for row in original_grid]

    # Identify start location
    (r, c), = ((r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '@')
    grid[r][c] = '.'

    # Execute all moves in sequence:
    for move in moves:
        dr, dc = dirs[move]
        r1 = r + dr
        c1 = c + dc
        if grid[r1][c1] == '.':
            # Move
            r, c = r1, c1
        else:
            # Try to push
            r2, c2 = r1, c1
            while grid[r2][c2] == 'O':
                r2 += dr
                c2 += dc
            if grid[r2][c2] == '.':
                grid[r1][c1] = '.'
                grid[r2][c2] = 'O'
                r, c = r1, c1
            else:
                assert grid[r2][c2] == '#'

    return CoordinateSum(grid, 'O')


def Part2():
    # Create expanded copy of the grid.
    expand = {
        '.': '..',
        '@': '@.',
        'O': '[]',
        '#': '##',
    }
    grid = [[ch2 for ch in row for ch2 in expand[ch]] for row in original_grid]

    # Identify start location
    (r, c), = ((r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '@')
    grid[r][c] = '.'

    # Helper function to push boxes vertically.
    def PushVertical(r, c, dr):
        todo = []
        seen = set()

        def MoveBox(r, c):
            ch = grid[r][c]
            if (r, c) not in seen:
                seen.add((r, c))
                todo.append((r, c))
                if ch == '[':
                    MoveBox(r, c + 1)
                else:
                    assert ch == ']'
                    MoveBox(r, c - 1)

        # Find all blocks that must move, recursively.
        MoveBox(r, c)
        for r, c in todo:
            ch = grid[r + dr][c]
            if ch == '#':
                return False
            if ch != '.':
                MoveBox(r + dr, c)

        # Move blocks in reverse order.
        for r, c in reversed(todo):
            assert grid[r + dr][c] == '.'
            grid[r + dr][c] = grid[r][c]
            grid[r][c] = '.'

        return True

    # Execute all moves in sequence:
    for move in moves:
        dr, dc = dirs[move]
        r1 = r + dr
        c1 = c + dc
        if grid[r1][c1] == '.':
            r, c = r1, c1
        elif grid[r1][c1] in '[]':
            if dr == 0:
                # (Try to) push horizontally.
                c2 = c1
                while grid[r][c2] in '[]':
                    c2 += dc
                if grid[r][c2] == '.':
                    if dc > 0: grid[r][c1+1:c2+1] = grid[r][c1:c2]
                    if dc < 0: grid[r][c2:c1] = grid[r][c2+1:c1+1]
                    grid[r][c1] = '.'
                    c = c1
                else:
                    assert grid[r][c2] == '#'

            else:
                # (Try to) push vertically.
                assert dc == 0
                if PushVertical(r1, c1, dr):
                    r = r1

    return CoordinateSum(grid, '[')


print(Part1())
print(Part2())
