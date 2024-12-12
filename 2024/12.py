# Advent of Code 2024 day 12: Garden Groups
# https://adventofcode.com/2024/day/12

import sys

grid = {(r, c): ch
        for r, line in enumerate(sys.stdin)
        for c, ch in enumerate(line.strip())}

# I model the positions along the perimeter with a coordinate pair (r,c) and
# a direction between 0 and 4 (exclusive), where the coordinates of a grid point
# correspond with the top-left corner of the corresponding square plot.
# 
#                0 (up)
#
#                ^
#      (r-1,c-1) | (r-1, c)
#                |
# 3 (left)  <----o---->  1 (right)
#                |
#      (r-1,c-1) | (r, c)
#                v
#
#              2 (down)
#

# Moves one step in the given direction:
def Step(v, dir):
    r, c = v
    if dir == 0: r -= 1
    if dir == 1: c += 1
    if dir == 2: r += 1
    if dir == 3: c -= 1
    return (r, c)

# Returns coordinates of the plots to the left and right of the given vertex and direction:
def GetFlanks(v, dir):
    r, c = v
    if dir == 0: return (r - 1, c - 1), (r - 1, c    )
    if dir == 1: return (r - 1, c    ), (r    , c    )
    if dir == 2: return (r    , c    ), (r    , c - 1)
    if dir == 3: return (r    , c - 1), (r - 1, c - 1)

# Traces an outline of a region. It is assumed the region to be traced lies on
# the right of (start, start_dir), but not on the left.
#
# To follow the outline, we can decide locally whether we can move forward or
# need to turn, based on the types of plots to the left and right of the current
# vertex/direction pair:
#
#   x   x
#     o--->  move forward
#   A   A
#
#   x   A
#     o--->  turn left   (we know the plot to the topleft is not `A`, or we
#   A   A                 would not have moved forward previous turn)
#
#   x   ?
#     o--->  turn right  (we know the plot to the bottomright must be `A`,
#   A   x                 or we would not have moved forward previous turn)
#
# Note that this function will only trace a single outline! If a region contains holes,
# they must be traced separately. (See TraceAllOutlines() below.)
def TraceOutline(start, start_dir):
    t = grid[start]
    outside = set()
    moves = 0
    turns = 0
    v, dir = start, start_dir
    while True:
        lv, rv = GetFlanks(v, dir)
        lc, rc = (grid.get(w) for w in (lv, rv))
        if lc == rc == t:
            dir = (dir - 1) % 4   # turn left
            turns += 1
        elif rc != t:
            dir = (dir + 1) % 4   # turn right
            turns += 1
        else:
            v = Step(v, dir)  # move forward
            assert rc == t and lc != t
            outside.add(lv)
            moves += 1
        if (v, dir) == (start, start_dir):
           return moves, turns, outside

# Traces all outlines of the given region; there is more than ones if the region
# contains holes. Note that holes do not exactly correspond with regions that
# are contained within:
#
#  AAA
#  AxA  has a hole in the middle (perimeter of 12 + 4 = 16)
#  AAA
#
#  AAx
#  AyA  does not have a hole in the middle; we can trace this as a
#  AAA  single continuous perimeter of length 16.
#
def TraceAllOutlines(region):
    total_moves = 0 
    total_turns = 0
    all_outside = set()
    for v in region:
        l, r = GetFlanks(v, 1)
        if grid.get(l) != grid[r] and l not in all_outside:
            moves, turns, outside = TraceOutline(v, 1)
            total_moves += moves
            total_turns += turns
            all_outside.update(outside)
    return (total_moves, total_turns)


filled = set()

def FloodFill(start):
    filled.add(start)
    region = [start]
    perimeter = 0
    for v in region:
        r, c = v
        for w in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
            if grid.get(w) != grid[v]:
                perimeter += 1
            elif w not in filled:
                filled.add(w)
                region.append(w)
    return region, perimeter


# Solve!
answer1 = 0
answer2 = 0
for v in grid:
    if v not in filled:
        # Part 1: flood fill to find area and perimeter
        region, perimeter = FloodFill(v)
        area = len(region)
        answer1 += area * perimeter

        # Part 2: trace outline of plot
        # (number of turns = number of straight line segments)
        moves, turns = TraceAllOutlines(region)
        assert moves == perimeter
        answer2 += area * turns
print(answer1)
print(answer2)
