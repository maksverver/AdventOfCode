import sys
from KnotHash import GetLengths, KnotHash, ReduceToInt

def Hash(string):
    return ReduceToInt(KnotHash(GetLengths(string)))

def IntToBits(i):
    return [(i >> j)&1 for j in range(SIZE)]

def Part1():
    return sum(sum(row) for row in GRID)

def Part2():
    def Clear(r, c):
        GRID[r][c] = 0
        for nr, nc in ((r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c)):
            if 0 <= nr < SIZE and 0 <= nc < SIZE and GRID[nr][nc]:
                Clear(nr, nc)
    regions = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if GRID[r][c]:
                Clear(r, c)
                regions += 1
    return regions

SIZE = 128
INPUT = sys.stdin.readline().strip()
GRID = [IntToBits(Hash('%s-%d'%(INPUT, row))) for row in range(SIZE)]

print(Part1())
print(Part2())
