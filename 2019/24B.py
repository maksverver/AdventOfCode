import sys

DIRS = ((-1, 0), (0, -1), (+1, 0), (0, +1))

bugs = set()
for r, line in enumerate(sys.stdin):
    for c, ch in enumerate(line):
        if ch == '#':
            bugs.add((r, c, 0))

def Neighbors(r, c, d):
    for (rr, cc) in ((r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)):
        if rr < 0:
            yield (1, 2, d - 1)
        elif rr >= 5:
            yield (3, 2, d - 1)
        elif cc < 0:
            yield (2, 1, d - 1)
        elif cc >= 5:
            yield (2, 3, d - 1)
        elif rr == 2 and cc == 2:
            if r == 1:
                assert c == 2
                for i in range(5):
                    yield (0, i, d + 1)
            if r == 3:
                assert c == 2
                for i in range(5):
                    yield (4, i, d + 1)
            if c == 1:
                assert r == 2
                for i in range(5):
                    yield (i, 0, d + 1)
            if c == 3:
                assert r == 2
                for i in range(5):
                    yield (i, 4, d + 1)
        else:
            yield (rr, cc, d)

def Next(bugs):
    cells = set((rr, cc, dd) for (r, c, d) in bugs for (rr, cc, dd) in Neighbors(r, c, d))
    new_bugs = set()
    for r, c, d in cells:
        old_bug = (r, c, d) in bugs
        neighbor_count = sum((rr, cc, dd) in bugs for (rr, cc, dd) in Neighbors(r, c, d))
        new_bug = neighbor_count == 1 if old_bug else neighbor_count in (1, 2)
        if new_bug:
            new_bugs.add((r, c, d))
    return new_bugs

for i in range(200):
    bugs = Next(bugs)
print(len(bugs))
