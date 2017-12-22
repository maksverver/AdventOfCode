from enum import Enum
import sys

class State(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

def Update1(s, dr, dc):
    if s == State.CLEAN:
        return State.INFECTED, -dc, dr  # turn left
    if s == State.INFECTED:
        return State.CLEAN, dc, -dr  # turn right

def Update2(s, dr, dc):
    if s == State.CLEAN:
        return State.WEAKENED, -dc, dr  # turn left
    if s == State.WEAKENED:
        return State.INFECTED, dr, dc
    if s ==  State.INFECTED:
        return State.FLAGGED, dc, -dr  # turn right
    if s == State.FLAGGED:
        return State.CLEAN, -dr, -dc  # turn around

def Solve(grid, iterations, update):
    states = {}
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '#':
                states[r, c] = State.INFECTED
    answer = 0
    r, c = len(grid)//2, len(grid[0])//2
    dr, dc = -1, 0
    for _ in range(iterations):
        s = states.get((r, c), State.CLEAN)
        s, dr, dc = update(s, dr, dc)
        if s == State.INFECTED:
            answer += 1
        states[r, c] = s
        r += dr
        c += dc
    return answer

grid = [line.strip() for line in sys.stdin]
print(Solve(grid, 10000, Update1))
print(Solve(grid, 10000000, Update2))
