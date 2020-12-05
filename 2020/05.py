import sys

def SeatId(s):
    r, c, h, w = 0, 0, 128, 8
    for ch in s:
        if ch in ('F', 'B'):
            h //= 2
            if ch == 'B':
                r += h
        elif ch in ('L', 'R'):
            w //= 2
            if ch == 'R':
                c += w
        else:
            assert False
    assert h == 1 and w == 1
    return 8*r + c

ids = set(SeatId(line.strip()) for line in sys.stdin)

# Part 1: maximum seat id
print(max(ids))

# Part 2: id of seat that isn't taken
print(*(i for i in range(min(ids), max(ids)) if i not in ids))
