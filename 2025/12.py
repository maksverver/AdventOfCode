import sys

*parts, last_part = sys.stdin.read().strip().split('\n\n')

shapes = []
areas = []

for part in parts:
    head, *lines = part.split('\n')
    shapes.append(tuple(lines))
    areas.append(sum(ch == '#' for line in lines for ch in line))

def Solve(h, w, counts):
    if (h // 3) * (w // 3) >= sum(counts):
        # We have enough space to place each box in its own
        # 3x3 rectangle, so a solution is definitely possible:
        return 1

    min_area = sum(c*a for c, a in zip(counts, areas))
    if min_area > h * w:
        # The total number of tiles needed for all boxes is
        # larger than the area of the floor, so a solution is
        # definitely impossible:
        return 0

    # If we get here, it's not obvious if a solution is possible or not.
    # Fortunately, this never happens in the official input (though it does
    # in the sample data!)
    print('Difficult:', h, w, counts, file=sys.stderr)
    assert False

answer = 0
for line in last_part.split('\n'):
    a, bs = line.split(': ')
    counts = [int(i) for i in bs.split()]
    assert(len(counts) == len(shapes))
    h, w = map(int, a.split('x'))
    answer += Solve(h, w, counts)
print(answer)
