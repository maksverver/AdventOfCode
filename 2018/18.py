import sys

def Next(grid):
    def NextCell(r, c):
        lumberyards = 0
        trees = 0
        for neighbour in (grid[rr][cc]
                for rr in (r - 1, r, r + 1) if 0 <= rr < len(grid)
                for cc in (c - 1, c, c + 1) if 0 <= cc < len(grid[rr]) and (rr != r or cc != c)):
            lumberyards += neighbour == '#'
            trees += neighbour == '|'
        cell = grid[r][c]
        if cell == '.':
            return '|' if trees >= 3 else '.'
        elif cell == '|':
            return '#' if lumberyards >= 3 else '|'
        elif cell == '#':
            return '#' if (lumberyards and trees) else '.'
    return tuple(tuple(NextCell(r, c) for c in range(len(row))) for r, row in enumerate(grid))

def Checksum(grid):
    string = ''.join(''.join(row) for row in grid)
    return string.count('|') * string.count('#')

def Solve(grid, steps):
    seen = {}
    for i in range(steps):
        if grid in seen:
            # Cycle detected!
            period = i - seen[grid]
            for _ in range((steps - i)%period):
                grid = Next(grid)
            break
        seen[grid] = i
        grid = Next(grid)
    return Checksum(grid)

grid = tuple(tuple(line.strip()) for line in sys.stdin)
print(Solve(grid, 10))
print(Solve(grid, 10**9))
