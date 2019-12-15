from enum import Enum
from intcode import Machine, MachineState
import sys

class Status(Enum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2
    UNKNOWN = 3

DIRS = ((-1, 0), (1, 0), (0, 1), (0, -1))

ints = list(map(int, sys.stdin.readline().split(',')))
machine = Machine(ints)
grid = {}

def PrintGrid(my_r, my_c, file=sys.stdout):
    '''Prints current grid state. For debugging.'''
    def GetCh(r, c):
        if r == my_r and c == my_c:
            return '@'
        return "#.O "[grid.get((r, c), Status.UNKNOWN).value]
    minr = maxr = minc = maxc = 0
    for (r, c) in grid.keys():
        minr = min(minr, r)
        minc = min(minc, c)
        maxr = max(maxr, r)
        maxc = max(maxc, c)
    for r in range(minr, maxr + 1):
        print(''.join(GetCh(r, c) for c in range(minc, maxc + 1)), file=file)

def TryMove(direction):
    assert 0 <= direction < 4
    machine.PutInput(direction + 1)
    state = machine.Run()
    assert state == MachineState.OUTPUT
    return machine.GetOutput()

def ReconstructPath(r, c, last_d, previous_dir):
    path = []
    while True:
        dr, dc = DIRS[last_d]
        path.append(last_d)
        r, c = r - dr, c - dc
        last_d = previous_dir[r, c]
        if last_d is None:
            break
    path.reverse()
    return path

def ShortestPath(r, c, is_goal):
    '''Finds the shortest path from (r, c) to a cell at (rr, cc), such that goal(rr, cc) is true.'''
    previous_dir = {(r, c): None}
    todo = [(r, c)]
    for (r, c) in todo:
        for d, (dr, dc) in enumerate(DIRS):
            rr, cc = r + dr, c + dc
            if is_goal(rr, cc):
                return ReconstructPath(rr, cc, d, previous_dir)
            if grid[rr, cc] == Status.WALL or (rr, cc) in previous_dir:
                continue
            previous_dir[rr, cc] = d
            todo.append((rr, cc))

def MaxDistance(r, c):
    '''Returns maximum length of a shortest path from (r, c) to another reachable cell.'''
    dist = {(r, c): 0}
    todo = [(r, c)]
    for (r, c) in todo:
        for (dr, dc) in DIRS:
            rr, cc = r + dr, c + dc
            if grid[rr, cc] == Status.WALL or (rr, cc) in dist:
                continue
            dist[rr, cc] = dist[r, c] + 1
            todo.append((rr, cc))
    return max(dist.values())

def ExploreGrid(r, c):
    grid[r, c] = Status.EMPTY
    while True:
        path = ShortestPath(r, c, lambda r, c: (r, c) not in grid)
        if path is None:
            return (r, c)
        for d in path[:-1]:
            dr, dc = DIRS[d]
            assert Status(TryMove(d)) == Status.EMPTY
            r, c = r + dr, c + dc
        d = path[-1]
        dr, dc = DIRS[d]
        rr, cc = r + dr, c + dc
        assert (rr, cc) not in grid
        grid[rr, cc] = status = Status(TryMove(d))
        if status != Status.WALL:
            r, c = rr, cc

end_r, end_c = ExploreGrid(0, 0)
#PrintGrid(end_r, end_c, file=sys.stderr)
(oxygen_r, oxygen_c), = (rc for (rc, status) in grid.items() if status == Status.OXYGEN)
print(len(ShortestPath(0, 0, lambda r, c: (r, c) == (oxygen_r, oxygen_c))))  # Part 1
print(MaxDistance(oxygen_r, oxygen_c))  # Part 2
