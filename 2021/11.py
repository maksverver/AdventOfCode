import sys

grid = [list(map(int, line.strip())) for line in sys.stdin]
H = len(grid)
W = len(grid[0])

def Neighbours(r, c):
    return [(rr, cc)
            for rr in [r - 1, r, r + 1]
            for cc in [c - 1, c, c + 1]
            if (rr, cc) != (r, c) and 0 <= rr < H and 0 <= cc < W]

def Step():
    flashed = [[False]*W for _ in range(H)]
    todo = []

    def Inc(r, c):
        if flashed[r][c]:
            return
        grid[r][c] += 1
        if grid[r][c] > 9:
            grid[r][c] = 0
            flashed[r][c] = True
            todo.append((r, c))

    for r in range(H):
        for c in range(W):
            Inc(r, c)

    for r, c in todo:
        for rr, cc in Neighbours(r, c):
            Inc(rr, cc)

    return len(todo)

# Part 1 
answer1 = 0
for _ in range(100):
    answer1 += Step()
print(answer1)

# Part 2 (assumes synchronization happens after step 100)
answer2 = 101
while Step() != H * W:
    answer2 += 1
print(answer2)
