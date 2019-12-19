# This solution assumes any path between two keys passes through the same set of
# doors (which seems to be the case).

from heapq import heappush, heappop
import sys

DIRS = ((-1, 0), (0, -1), (0, 1), (1, 0))

GRID = [line.rstrip() for line in sys.stdin]
H = len(GRID)
W = len(GRID[0])
assert all(len(row) == W for row in GRID)

KEYS = ''.join(sorted(ch for row in GRID for ch in row if ch.islower()))

def FindChar(target):
    (r, c), = [(r, c) for r, row in enumerate(GRID) for c, ch in enumerate(row) if ch == target]
    return (r, c)

key_locs = dict((key, FindChar(key)) for key in KEYS)

def AddChar(s, ch):
    return ''.join(sorted(s + ch))

def CalculateDistancesAndDoors(start_locs):
    "Returns a dictionary (src, dst) -> (distance, needed keys)"
    dists = {}
    for src in start_locs + KEYS:
        (r, c), = [(r, c) for r, row in enumerate(GRID) for c, ch in enumerate(row) if ch == src]
        seen = {}
        seen[r, c] = (0, '')
        todo = [(r, c)]
        for r, c in todo:
            dist, needed = seen[r, c]
            new_dist = dist + 1
            for dr, dc in DIRS:
                rr, cc = r + dr, c + dc
                if GRID[rr][cc] == '#':
                    continue
                if (rr, cc) in seen:
                    continue
                ch = GRID[rr][cc]
                if ch.isupper():
                    assert ch.lower() not in needed
                    new_needed = AddChar(needed, ch.lower())
                else:
                    new_needed = needed
                if ch.islower():
                    assert (src, ch) not in dists
                    dists[src, ch] = (new_dist, new_needed)
                seen[rr, cc] = (new_dist, new_needed)
                todo.append((rr, cc))
    return dists

def IsSubset(a, b):
    for ch in a:
        if ch not in b:
            return False
    return True

def FindShortestPath(start_locs):
    "Find shortest path to collect all keys using Dijkstra's algorithm."
    # (src, dst) -> (distance, needed keys)
    DISTS = CalculateDistancesAndDoors(start_locs)
    min_dists = {}
    min_dists[(start_locs, '')] = 0
    todo = [(0, start_locs, '')]
    while todo:
        dist, locs, have = heappop(todo)
        if dist > min_dists[locs, have]:
            continue
        if len(have) == len(KEYS):
            return dist
        for key in KEYS:
            if key in have:
                continue
            for i, loc in enumerate(locs):
                if (loc, key) in DISTS:
                    add_dist, need = DISTS[loc, key]
                    if IsSubset(need, have):
                        new_dist = dist + add_dist
                        new_locs = locs[:i] + key + locs[i + 1:]
                        new_have = AddChar(have, key)
                        old_dist = min_dists.get((new_locs, new_have), None)
                        if old_dist is None or new_dist < old_dist:
                            min_dists[new_locs, new_have] = new_dist
                            heappush(todo, (new_dist, new_locs, new_have))

# Part 1
print(FindShortestPath('@'))

# Update map for part 2
#
#   ...      1#2
#   .@.  =>  ###
#   ...      3#4
#
r, c = FindChar('@')
assert GRID[r - 1][c - 1:c + 2] == '...'
assert GRID[r    ][c - 1:c + 2] == '.@.'
assert GRID[r + 1][c - 1:c + 2] == '...'
GRID[r - 1] = GRID[r - 1][:c - 1] + '1#2' + GRID[r - 1][c + 2:]
GRID[r    ] = GRID[r    ][:c - 1] + '###' + GRID[r    ][c + 2:]
GRID[r + 1] = GRID[r + 1][:c - 1] + '3#4' + GRID[r + 1][c + 2:]

# Part 2
print(FindShortestPath('1234'))
