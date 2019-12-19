from intcode import ReadInts, RunInteractive

ints = ReadInts()

DIRS = ((-1, 0), (0, -1), (1, 0), (0, 1))

def Paint(tiles):
    command_index = 0
    r, c, dir = 0, 0, 0

    def GetTile():
        return tiles.get((r, c), 0)

    def ExecuteInstruction(i):
        nonlocal r, c, dir, command_index
        assert i in (0, 1)
        if command_index == 0:
            tiles[(r, c)] = i
        else:
            if i == 0:
                dir += 1
            else:
                dir -= 1
            dir %= 4
            dr, dc = DIRS[dir]
            r += dr
            c += dc
        command_index ^= 1

    RunInteractive(ints, GetTile, ExecuteInstruction)
    return tiles

def PrintTiles(tiles):
    minr = minc = maxr = maxc = 0
    for (r, c) in tiles:
        minr = min(minr, r)
        minc = min(minc, c)
        maxr = max(maxr, r)
        maxc = max(maxc, c)
    for r in range(minr, maxr + 1):
        print(''.join('.#'[tiles.get((r, c), 0)] for c in range(minc, maxc + 1)))

# Part 1
print(len(Paint({})))

# Part 2
PrintTiles(Paint({(0, 0): 1}))
