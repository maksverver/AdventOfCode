from collections import defaultdict
from functools import reduce
from operator import mul
import sys

def ParseTile(part):
    header, *rows = part.split('\n')
    assert header.startswith('Tile ') and header.endswith(':')
    tile_id = int(header[5:-1])
    return (tile_id, rows)

def GetSides(grid):
    return [grid[0] for grid in Transformations(grid)]

def Rotate(grid):
    return [''.join(grid[c][r] for c in range(len(grid))) for r in range(len(grid[0]) - 1, -1, -1)]

def Flip(grid):
    return [''.join(grid[c][r] for c in range(len(grid))) for r in range(len(grid[0]))]

def Transformations(grid):
    a = grid
    b = Rotate(a)
    c = Rotate(b)
    d = Rotate(c)
    e = Flip(a)
    f = Rotate(e)
    g = Rotate(f)
    h = Rotate(g)
    return [a, b, c, d, e, f, g, h]

def Other(ids, id):
    a, b = ids
    return a if id == b else b

TopSide    = lambda grid: grid[0]
LeftSide   = lambda grid: ''.join(row[0] for row in grid)
BottomSide = lambda grid: grid[-1]
RightSide  = lambda grid: ''.join(row[-1] for row in grid)

# (tile_id -> [row])
tiles = dict(map(ParseTile, sys.stdin.read().strip().split('\n\n')))

# Part 1: find corner tiles, and print product of their ids.
tile_sides = [(tile_id, GetSides(grid)) for (tile_id, grid) in tiles.items()]
tiles_by_side = defaultdict(list)  # side -> [tile_id]
for tile, sides in tile_sides:
    for side in sides:
        tiles_by_side[side].append(tile)

# Sanity check: each side can match at most two tiles (one at the edge)
for side in tiles_by_side.values():
    assert len(side) in (1, 2)

corners = [tile for tile, sides in tile_sides
    if sum(len(tiles_by_side[side]) > 1 for side in sides) == 4]
assert(len(corners) == 4)
print(reduce(mul, corners))


#
# Part 2: reconstruct the image and find the sea monsters!
#

def MakeComposite():
    # Size of the composite grid (i.e. number of tiles along each side).
    # This assumes the result is a square (which it is!)
    S = int(len(tiles)**.5)
    assert S**2 == len(tiles)

    composite_tile_ids = [[None]*S for _ in range(S)]
    composite_subgrids = [[None]*S for _ in range(S)]
    for r in range(S):
        for c in range(S):
            if r == 0 and c == 0:
                # Place topleft corner so that adjacent tiles connect at the
                # right and bottom side. There are two mirrored solutions.
                tile_id = corners[0]
                [grid, _] = [grid for grid in Transformations(tiles[tile_id])
                        if (len(tiles_by_side[RightSide(grid)]) == 2 and 
                            len(tiles_by_side[BottomSide(grid)]) == 2)]
            elif c == 0:
                # Match tile above.
                side = BottomSide(composite_subgrids[r - 1][c])
                tile_id = Other(tiles_by_side[side], composite_tile_ids[r - 1][c])
                grid, = [grid for grid in Transformations(tiles[tile_id]) if TopSide(grid) == side]
            else:
                # Match tile to the left.
                side = RightSide(composite_subgrids[r][c - 1])
                tile_id = Other(tiles_by_side[side], composite_tile_ids[r][c - 1])
                grid, = [grid for grid in Transformations(tiles[tile_id]) if LeftSide(grid) == side]
                if r > 0:
                    assert TopSide(grid) == BottomSide(composite_subgrids[r - 1][c])

            composite_subgrids[r][c] = grid
            composite_tile_ids[r][c] = tile_id

    L = 8  # size of subgrids
    return [''.join(composite_subgrids[r // L][c // L][r % L + 1][c % L + 1]
                for c in range(S * L))
                for r in range(S * L)]

def FindMonsters(grid):
    monster = [
        '..................#.',
        '#....##....##....###',
        '.#..#..#..#..#..#...']

    coords = [(r, c) for r, row in enumerate(monster) for c, ch in enumerate(row) if ch == '#']

    monster_cells = set()
    for r in range(len(grid) - len(monster) + 1):
        for c in range(len(grid[0]) - len(monster[0]) + 1):
            if all(grid[r + i][c + j] == '#' for (i, j) in coords):
                for i, j in coords:
                    monster_cells.add((r + i, c + j))
    return monster_cells

for grid in Transformations(MakeComposite()):
    monster_cells = FindMonsters(grid)
    if monster_cells:
        # Save monsters found for debugging.
        #with open('monsters.txt', 'wt') as f:
        #    for i, row in enumerate(grid):
        #        print(''.join([ch, 'o'][(i, j) in monster_cells] for j, ch in enumerate(row)), file=f)

        # Calculate answer: number of #s in the grid that are not part of a monster.
        answer = sum(ch == '#' and (r, c) not in monster_cells
            for r, row in enumerate(grid) for c, ch in enumerate(row))
        print(answer)
