import sys

grid = [list(line.strip()) for line in sys.stdin]

H = len(grid)
W = len(grid[0])

def Iterate(grid, adj, max_neighbors):
    def GetCell(i, j):
        value = grid[i][j]
        if value == '.':
            return '.'
        neighbors = sum(grid[r][c] == '#' for (r, c) in adj[i][j])
        if value == 'L' and neighbors == 0:
            return '#'
        if value == '#' and neighbors > max_neighbors:
            return 'L'
        return value
    return [[GetCell(i, j) for j in range(W)] for i in range(H)]

def Solve(grid, adj, max_neighbors):
    prev_grid = None
    while grid != prev_grid:
        # print(*(''.join(row) for row in grid), sep='\n', end='\n\n')
        prev_grid = grid
        grid = Iterate(grid, adj, max_neighbors)
    return sum(value == '#' for row in grid for value in row)

def Adjacent1(i, j):
    return [(r,c)
        for r in range(max(0, i - 1), min(i + 2, H))
        for c in range(max(0, j - 1), min(j + 2, W))
        if (r, c) != (i, j)]

def Adjacent2(i, j):
    adj = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if (dr, dc) != (0, 0):
                r, c = i + dr, j + dc
                while 0 <= r < H and 0 <= c < W:
                    if grid[r][c] != '.':
                        adj.append((r, c))
                        break
                    r, c = r + dr, c + dc
    return adj

ADJ1 = [[Adjacent1(i, j) for j in range(W)] for i in range(H)]
ADJ2 = [[Adjacent2(i, j) for j in range(W)] for i in range(H)]

print(Solve(grid, ADJ1, 3))
print(Solve(grid, ADJ2, 4))
