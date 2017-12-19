import sys

maze = list(sys.stdin)
r, c = 0, maze[0].index('|')
dr, dc = 1, 0
letters = ''
steps = 0
while maze[r][c] != ' ':
    if maze[r][c] == '+':
        if maze[r - dc][c + dr] == ' ':
            dr, dc = dc, -dr
        else:
            dr, dc = -dc, dr
    elif maze[r][c].isalpha():
        letters += maze[r][c]
    r += dr
    c += dc
    steps += 1
print(letters)
print(steps)
