from intcode import ReadInts, RunMachine
import sys

DIRS = (
    (-1,  0),   # up
    ( 0, +1),   # right
    (+1,  0),   # down
    ( 0, -1),   # left
)
DIR_CHARS = '^>v<'

ints = ReadInts()
grid = ''.join(map(chr, RunMachine(ints, []))).rstrip('\n').split('\n')
H = len(grid)
W = len(grid[0])

def Step(r, c, d):
    dr, dc = DIRS[d]
    return r + dr, c + dc

def FindSimplePath():
    'Finds a path by going straight through every intersection, never backtracking.'
    # state[r][c] is the number of times we still need to cover cell (r, c); either 0, 1 or 2
    state = [[int(grid[r][c] == '#') for c in range(W)] for r in range(H)]
    alignment = 0
    for r in range(1, H - 1):
        for c in range(1, W - 1):
            if (state[r][c] and state[r - 1][c] and state[r + 1][c] and
                    state[r][c - 1] and state[r][c + 1]):
                # Intersections will be crossed twice.
                state[r][c] += 1
                alignment += r*c

    def Look(r, c, d):
        rr, cc = Step(r, c, d)
        if 0 <= rr < H and 0 <= cc < W:
            return state[rr][cc]
        return 0

    # Find initial position and direction.
    # We assume we start at the end of a corridoor.
    ((r, c),) = [(r, c) for r in range(H) for c in range(W) if grid[r][c] in DIR_CHARS]
    d = DIR_CHARS.index(grid[r][c])

    # Find path!
    instructions = []
    while True:
        ahead = 0
        while Look(r, c, d):
            r, c = Step(r, c, d)
            state[r][c] -= 1
            ahead += 1
        if ahead > 0:
            instructions.append(str(ahead))
        dl = (d - 1)%4
        dr = (d + 1)%4
        if Look(r, c, dl):
            d = dl
            instructions.append('L')
        elif Look(r, c, dr):
            d = dr
            instructions.append('R')
        else:
            # Check that we covered the entire grid.
            assert all(state[r][c] == 0 for r in range(H) for c in range(W))
            break

    return alignment, instructions

def SplitIntoChunks(instrs):
    def Search(chunks, main, pos):
        if pos == len(instrs):
            return chunks, main
        for i, chunk in enumerate(chunks):
            end = pos + len(chunk)
            if end <= len(instrs) and instrs[pos:end] == chunk:
                result = Search(chunks, main + (i,), end)
                if result:
                    return result
        if len(chunks) < 3:
            end = pos + 1
            for end in range(pos + 1, len(instrs)):
                if len(','.join(instrs[pos:end])) > 20:
                    break
                result = Search(chunks + (instrs[pos:end],), main + (len(chunks),), end)
                if result:
                    return result

    return Search((), (), 0)

alignment, instructions = FindSimplePath()
chunks, main = SplitIntoChunks(instructions)

assert instructions == [cmd for i in main for cmd in chunks[i]]
assert len(chunks) == 3  # if it's less, we need to pad it with empty chunks

DEBUG = False
ints[0] = 2
input_str = (
        ','.join("ABC"[i] for i in main) + '\n' +
        ','.join(chunks[0]) + '\n' +
        ','.join(chunks[1]) + '\n' +
        ','.join(chunks[2]) + '\n' +
        'ny'[DEBUG] + '\n')

output = RunMachine(ints, tuple(map(ord, input_str)))
if DEBUG:
    sys.stdout.write(''.join(map(chr, output[:-1])))

print(alignment)   # Part 1
print(output[-1])  # Part 2
