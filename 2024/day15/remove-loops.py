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

moves_to_keep = []

grid = grid2
(r, c), = ((r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '@')
grid[r][c] = '.'

positions = []
visited = set()
output = []

for i, move in enumerate(moves):
    pos = (r, c)
    while pos in visited:
        old_pos = positions.pop()
        assert old_pos in visited
        visited.remove(old_pos)
        output.pop()

    if i > 0 and i % 100000 == 0:
        print('%.2f%% done (output %.2f%%)' % (100.0 * i / len(moves), 100 * len(output) / i), file=sys.stderr)

    positions.append(pos)
    visited.add(pos)
    output.append(move)

    dr, dc = dirs[move]
    r1 = r + dr
    c1 = c + dc
    if grid[r1][c1] == '.':
        r, c = r1, c1
    elif grid[r1][c1] != '#':
        if dr == 0 and PushHorizontal(r1, c1, dc):
            c = c1
            positions = []
            visited = set()
        elif dc == 0 and PushVertical(r1, c1, dr):
            r = r1
            positions = []
            visited = set()

print(grid_data)
print()
print(''.join(output))

