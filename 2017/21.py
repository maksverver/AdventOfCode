from collections import Counter
import sys

INITIAL_TILE = [
    '.#.',
    '..#',
    '###']

def Rotate(tile):
    N = len(tile)
    return [''.join(tile[N - 1 - c][r] for c in range(N)) for r in range(N)]

def Mirror(tile):
    return list(reversed(tile))

def Variants(grid):
    for _ in range(2):
        for _ in range(4):
            yield grid
            grid = Rotate(grid)
        grid = Mirror(grid)

def Id(grid):
    return tuple(min(Variants(grid)))

def ExtractTile(grid, r, c, size):
    return [grid[i][c:c + size] for i in range(r, r + size)]

def Transform(grid):
    N = len(grid)  # size of grid
    S = 2 + N%2    # size of input tiles
    T = S + 1      # size of output tiles
    # Break grid into 2D array of tiles (each tile a list of strings)
    tiles = [[ExtractTile(grid, i, j, S) for j in range(0, N, S)]
        for i in range(0, N, S)]
    # Transform tiles using mapping
    tiles = [[mapping[Id(tile)] for tile in row] for row in tiles]
    # Combine tiles into grid (list of strings)
    return [''.join(tiles[i//T][j//T][i%T][j%T] for j in range(N//S*T))
        for i in range(N//S*T)]

def SolveSlowly(grid, iterations):
    for _ in range(iterations):
        grid = Transform(grid)
    return sum(row.count('#') for row in grid)

def Part2():
    mapping3 = {}
    for src, dst in mapping.items():
        if len(src) == 3:
            assert len(dst) == 4
            dst = Transform(Transform(dst))
            assert len(dst) == 9
            mapping3[src] = Counter(
                Id([dst[3*i + k][3*j:3*j + 3] for k in range(3)])
                for i in range(3) for j in range(3))
    counts = Counter({Id(INITIAL_TILE): 1})
    for _ in range(18 // 3):
        new_counts = Counter()
        for tile, count in counts.items():
            for new_tile, new_count in mapping3[tile].items():
                new_counts[new_tile] += count*new_count
        counts = new_counts
    return sum(
        count*sum(row.count('#') for row in tile)
        for tile, count in counts.items())

def Solve(iterations):
    counts = Counter({Id(INITIAL_TILE): 1})
    for _ in range(iterations//3):
        new_counts = Counter()
        for tile, count in counts.items():
            for new_tile, new_count in mapping3[tile].items():
                new_counts[new_tile] += count*new_count
        counts = new_counts
    answer = 0
    for tile, count in counts.items():
        for _ in range(iterations%3):
            tile = Transform(tile)
        answer += count*sum(row.count('#') for row in tile)
    return answer

# Maps canonical tile to the grid after 1 step.
mapping = {}
for line in sys.stdin:
    src, dst = line.strip().split(' => ')
    src = src.split('/')
    dst = dst.split('/')
    mapping[Id(src)] = dst

# Maps canonical 3x3 tile to a counter of 3x3 tiles after 3 steps.
mapping3 = {}
for src, dst in mapping.items():
    if len(src) == 3:
        assert len(dst) == 4
        dst = Transform(Transform(dst))
        assert len(dst) == 9
        mapping3[src] = Counter(
            Id([dst[3*i + k][3*j:3*j + 3] for k in range(3)])
            for i in range(3) for j in range(3))

print(Solve(5))
print(Solve(18))
