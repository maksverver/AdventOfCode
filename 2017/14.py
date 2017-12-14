import sys
from KnotHash import GetLengths, KnotHash, ReduceToInt

def MakeGrid(input):
    def HashRow(row):
        return ReduceToInt(KnotHash(GetLengths('%s-%d'%(input, row))))
    def IntToBits(i):
        return [(i >> j)&1 for j in range(SIZE)]
    return [IntToBits(HashRow(row)) for row in range(SIZE)]

def Part1():
    return sum(sum(row) for row in GRID)

def Part2():
    def Clear(r, c):
        '''Clears the bit at (r, c) and all adjacent ones. Modifies the global
        GRID, which is not very nice, but meh.'''
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
GRID = MakeGrid(sys.stdin.readline().strip())
print(Part1())
print(Part2())
