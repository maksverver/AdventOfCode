import hashlib
import sys

# Super fast way to read the input
data = sys.stdin.read()
H = data.count('\n')
W = data.index('\n')
data = data.replace('\n', '').replace('.', '0')
right = int(data.replace('>', '1').replace('v', '0'), 2)
down = int(data.replace('>', '0').replace('v', '1'), 2)

def Bit(r, c):
    return 1 << (r*W + c)

all_mask = (1 << (H * W)) - 1

top_mask = sum(Bit(H - 1, c) for c in range(W))
bot_mask = sum(Bit(0, c)     for c in range(W))
lft_mask = sum(Bit(r, W - 1) for r in range(H))
rgt_mask = sum(Bit(r, 0)     for r in range(H))

not_top_mask = top_mask ^ all_mask
not_bot_mask = bot_mask ^ all_mask
not_lft_mask = lft_mask ^ all_mask
not_rgt_mask = rgt_mask ^ all_mask

def RotLeft(mask):
    return ((mask & not_lft_mask) << 1) | ((mask & lft_mask) >> (W - 1))

def RotRight(mask):
    return ((mask & not_rgt_mask) >> 1) | ((mask & rgt_mask) << (W - 1))

def RotUp(mask):
    return ((mask & not_top_mask) << W) | ((mask & top_mask) >> (H - 1)*W)

def RotDown(mask):
    return ((mask & not_bot_mask) >> W) | ((mask & bot_mask) << (H - 1)*W)

def MoveRight(right, down):
    free = (right | down) ^ all_mask
    move = right & RotLeft(free)
    return right ^ move ^ RotRight(move)

def MoveDown(right, down):
    free = (right | down) ^ all_mask
    move = down & RotUp(free)
    return down ^ move ^ RotDown(move)

# Print grid (for debugging)
def Print(right, down):
    for r in range(H):
        line = ''
        for c in range(W):
            if right & Bit(r, c):
                line += '>'
            elif down & Bit(r, c):
                line += 'v'
            else:
                line += '.'
        print(line)
    print()

def Solve(right, down):
    steps = 0
    last_right = last_down = None
    while right != last_right or down != last_down:
        last_right = right
        last_down = down
        right = MoveRight(right, down)
        down = MoveDown(right, down)
        steps += 1
    return steps

def Verify(right, down):
    seen = set()
    last = None
    while (right, down) not in seen:
        seen.add((right, down))
        last = (right, down)
        right = MoveRight(right, down)
        down = MoveDown(right, down)
    if last != (right, down):
        print('Cycle detected!')
        sys.exit(1)
    return len(seen)

print(Solve(right, down))

# Verify() is a slightly-slower version of Solve() that detects inputs that
# repeat indefinitely. Can be used to verify randomly-generated grids are valid.
#print(Verify(right, down))
