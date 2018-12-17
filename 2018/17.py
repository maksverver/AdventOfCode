from collections import deque
import re
import sys

lines = []
for line in sys.stdin:
    m = re.match(r'x=(\d+), y=(\d+)[.][.](\d+)$', line)
    if m:
        x, y1, y2 = map(int, m.groups())
        assert y1 < y2
        lines.append((x, y1, x, y2))
        continue
    m = re.match(r'y=(\d+), x=(\d+)[.][.](\d+)$', line)
    if m:
        y, x1, x2 = map(int, m.groups())
        assert x1 < x2
        lines.append((x1, y, x2, y))
        continue
    assert False

min_x = min(x1 for (x1, y1, x2, y2) in lines) - 3
max_x = max(x2 for (x1, y1, x2, y2) in lines) + 3
min_y = min(y1 for (x1, y1, x2, y2) in lines)
max_y = max(y2 for (x1, y1, x2, y2) in lines)
faucet_x = 500 - min_x
lines = [(x1 - min_x, y1, x2 - min_x, y2) for (x1, y1, x2, y2) in lines]
W = max_x - min_x + 1
H = max_y + 2
assert 0 < faucet_x < W - 1

grid = [['.']*W for _ in range(H)]
for (x1, y1, x2, y2) in lines:
    if x1 == x2:
        for y in range(y1, y2 + 1):
            grid[y][x1] = '#'
    else:
        assert y1 == y2
        for x in range(x1, x2 + 1):
            grid[y1][x] = '#'

def Change(r, c, ch):
    assert grid[r][c] != ch
    assert grid[r][c] in '.<|>'
    assert ch in '<|>~'
    if c == 1:
        print(r,c)
    grid[r][c] = ch
    dirty.update((rr, cc) for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2) if 0 < rr < H - 1)

dirty = set()
grid[0][faucet_x] = '|'
dirty.add((1, faucet_x))

while dirty:
    r, c = dirty.pop()
    assert r - 1 >= 0
    assert c - 1 >= 0 and c + 1 < W
    if grid[r][c] == '.':
        if grid[r - 1][c] in '<|>':
            Change(r, c, '|')
        elif grid[r][c - 1] in '|>' and grid[r + 1][c - 1] in '#~':
            Change(r, c, grid[r][c - 1])
        elif grid[r][c + 1] in '<|' and grid[r + 1][c + 1] in '#~':
            Change(r, c, grid[r][c + 1])
    elif grid[r][c] == '|':
        if grid[r][c - 1] == '~' or grid[r][c + 1] == '~':
            Change(r, c, '~')
        elif grid[r + 1][c] in '~#':
            if grid[r][c - 1] in '#>':
                Change(r, c, '>')
            elif grid[r][c + 1] in '<#':
                Change(r, c, '<')
    elif ((grid[r][c] == '>' and grid[r][c + 1] in '~<#') or
            (grid[r][c] == '<' and grid[r][c - 1] in '~>#')):
        Change(r, c, '~')

# Part 1
print(sum(ch in '~|<>' for row in grid[min_y:max_y + 1] for ch in row))

# Part 2
print(sum(row.count('~') for row in grid[min_y:max_y + 1]))

# For debugging:
#print(*(''.join(row) for row in grid), sep='\n', file=open('day17.txt','wt'))

# For visualization:
def SaveImage(filename):
    from PIL import Image
    im = Image.new('P', (W, H))
    palette = 3*256*[0]
    palette[ 0: 3] = (255, 224, 160)  # 0: sand
    palette[ 3: 6] = ( 32,  32,  32)  # 1: clay
    palette[ 6: 9] = (  0,   0, 244)  # 2: standing water
    palette[ 9:12] = (128, 160, 255)  # 3: flowing water
    palette[12:15] = (  0, 255,   0)  # 4: faucet
    im.putpalette(palette)
    colormap = {'.': 0, '#': 1, '~': 2, '<': 3, '|': 3, '>': 3, '+': 4}
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            im.putpixel((x, y), colormap[ch])
    im = im.resize((5*W, 5*H))
    im.save(filename)
#SaveImage('day17.png')
