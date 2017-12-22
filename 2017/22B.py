from collections import defaultdict
from enum import Enum
import sys

class State(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

def Solve(grid, iterations):
    state = defaultdict(lambda: State.CLEAN)
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '#':
                state[r, c] = State.INFECTED
    answer = 0
    r, c = len(grid)//2, len(grid[0])//2
    dr, dc = -1, 0
    for _ in range(iterations):
        st = state[r, c]
        if st == State.CLEAN:
            st = State.WEAKENED
            dr, dc = -dc, dr  # turn left
        elif st == State.WEAKENED:
            st = State.INFECTED
            answer += 1
        elif st == State.INFECTED:
            st = State.FLAGGED
            dr, dc = dc, -dr  # turn right
        elif st == State.FLAGGED:
            st = State.CLEAN
            dr, dc = -dr, -dc  # reverse direction
        else:
            assert False
        state[r, c] = st
        r += dr
        c += dc
    return answer

grid = [line.strip() for line in sys.stdin]
print(Solve(grid, 10000000))
