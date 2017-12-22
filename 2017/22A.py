from collections import defaultdict
import sys

def Solve(grid, iterations):
    infected = defaultdict(lambda: False)
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            infected[r, c] = val == '#'
    answer = 0
    r, c = len(grid)//2, len(grid[0])//2
    dr, dc = -1, 0
    for _ in range(iterations):
        if infected[r, c]:
            dr, dc = dc, -dr  # turn right
            infected[r, c] = False
        else:
            dr, dc = -dc, dr  # turn left
            infected[r, c] = True
            answer += 1
        r += dr
        c += dc
    return answer

grid = [line.strip() for line in sys.stdin]
print(Solve(grid, 10000))
