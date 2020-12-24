import sys

DIR = {
    'nw': (-1, -1),
    'ne': (-1,  0),
    'w':  ( 0, -1),
    'e':  ( 0,  1),
    'sw': ( 1,  0),
    'se': ( 1,  1)}

def Tokenize(line):
    prev = None
    for char in line:
        if char in 'ns':
            assert not prev
            prev = char
        elif char in 'ew':
            if prev:
                yield prev + char
                prev = None
            else:
                yield char
        else:
            assert False
    assert not prev

def ParseCoords(line):
    r, c = 0, 0
    for tok in Tokenize(line.strip()):
        dr, dc = DIR[tok]
        r += dr
        c += dc
    return (r, c)

def Neighbours(p):
    r, c = p
    return [(r + dr, c + dc) for (dr, dc) in DIR.values()]

def Simulate(flipped, iterations):
    def CountFlippedNeighbors(p):
        return sum(q in flipped for q in Neighbours(p))

    for _ in range(iterations):
        unflipped = set(
            [q for p in flipped for q in Neighbours(p) if q not in flipped])
        flipped = set(
            [p for p in flipped if CountFlippedNeighbors(p) in (1, 2)] +
            [p for p in unflipped if CountFlippedNeighbors(p) == 2])

    return flipped

initial_flipped = set()
for line in sys.stdin:
    p = ParseCoords(line)
    if p in initial_flipped:
        initial_flipped.remove(p)
    else:
        initial_flipped.add(p)

# Part 1: count of tiles flipped initially
print(len(initial_flipped))

# Part 2: count of tiles flipped after 100 iterations.
print(len(Simulate(initial_flipped, 100)))
