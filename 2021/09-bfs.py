import sys

grid = [[int(c) for c in line.strip()] for line in sys.stdin]
H = len(grid)
W = len(grid[0])

def Neighbors(r, c):
    return [(rr, cc) for (rr, cc) in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)] if 0 <= rr < H and 0 <= cc < W]

def Part1():
    answer = 0
    for r in range(H):
        for c in range(W):
            if all(grid[rr][cc] > grid[r][c] for (rr, cc) in Neighbors(r, c)):
                answer += grid[r][c] + 1
    return answer

def FindBasinSizes():
    blocked = [[grid[r][c] == 9 for c in range(W)] for r in range(H)]
    for r in range(H):
        for c in range(W):
            if not blocked[r][c]:
                blocked[r][c] = True
                todo = [(r,c)]
                for r, c in todo:
                    for (rr, cc) in Neighbors(r, c):
                         if not blocked[rr][cc]:
                            blocked[rr][cc] = True
                            todo.append((rr, cc))
                yield len(todo)

def Part2():
    a, b, c = sorted(FindBasinSizes())[-3:]
    return a * b * c

print(Part1())
print(Part2())
