import sys
from heapq import heappush, heappop

# Puzzle shape (for part 1)
#
#     0123456789012
#   0 #############
#   1 #...........#
#   2 ###A#B#C#D###
#   3   #A#B#C#D#
#   4   #########

move_cost = {
    'A':    1,
    'B':   10,
    'C':  100,
    'D': 1000,
}

column_by_type = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9,
}

type_by_column = {v: k for k, v in column_by_type.items()}


def PathLen(r1, c1, r2, c2):
    '''Length path from (r1, c1) to (r2, c2) assuming the path isn't blocked.
       Assumes the shape of the level.'''
    return abs(r2 - r1) + abs(c2 - c1)


def IsTopRowFree(grid, c1, c2):
    if c1 <= c2:
        while c1 != c2:
            c1 += 1
            if grid[1][c1] != '.':
                return False
        return True
    else:
        while c1 != c2:
            c1 -= 1
            if grid[1][c1] != '.':
                return False
        return True


def IsSolved(grid):
    return all(grid[r][c] == ch
        for ch, c in column_by_type.items()
        for r in range(2, len(grid) - 1))


def Move(grid, r1, c1, r2, c2):
    assert grid[r1][c1] != '.'
    assert grid[r2][c2] == '.'
    sch = grid[r1][c1]
    cost = PathLen(r1, c1, r2, c2) * move_cost[sch]
    new_grid = list(grid)
    new_grid[r2] = new_grid[r2][:c2] + sch + new_grid[r2][c2+1:]
    new_grid[r1] = new_grid[r1][:c1] + '.' + new_grid[r1][c1+1:]
    return (cost, tuple(new_grid))


def Successors(grid):
    successors = []
    for ch, c in column_by_type.items():
        r = len(grid) - 2
        while r > 1 and grid[r][c] == ch:
            r -= 1
        if r > 1:
            s = 2
            while s <= r and grid[s][c] == '.':
                s += 1
            if s <= r:
                # Move out of column c
                assert grid[s][c] in 'ABCD'
                for d, dh in enumerate(grid[1]):
                    if dh == '.' and d not in type_by_column and IsTopRowFree(grid, c, d):
                        successors.append(Move(grid, s, c, 1, d))
            else:
                # Move into column c
                assert grid[r][c] == '.'
                for d, dh in enumerate(grid[1]):
                    if ch == dh and IsTopRowFree(grid, d, c):
                        # If we can move a piece to its destination, it is always
                        # optimal to do so, so don't consider other options:
                        return [Move(grid, 1, d, r, c)]
    return successors


def Solve(initial_grid):
    # Dijkstra's algorithm
    inf = float('inf')
    min_cost = {initial_grid: 0}
    pq = [(0, initial_grid)]
    while pq:
        cost, grid = heappop(pq)
        if cost != min_cost[grid]:
            continue
        if IsSolved(grid):
            return cost
        for c, next_grid in Successors(grid):
            next_cost = cost + c
            if next_cost < min_cost.get(next_grid, inf):
                min_cost[next_grid] = next_cost
                heappush(pq, (next_cost, next_grid))


def Enlarge(grid):
    return (
        grid[:3] + (
            '  #D#C#B#A#  ',
            '  #D#B#A#C#  ',
        ) + grid[3:]
    )


grid = tuple(line.rstrip() for line in sys.stdin)
print(Solve(grid))            # Part 1
print(Solve(Enlarge(grid)))   # Part 2
