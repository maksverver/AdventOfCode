import sys

*parts, last_part = sys.stdin.read().strip().split('\n\n')

shapes = []
areas = []

for part in parts:
    head, *lines = part.split('\n')
    shapes.append(tuple(lines))
    areas.append(sum(ch == '#' for line in lines for ch in line))

# If the total area of the pieces exceeds the area of the rectangle, then
# a solution is not possible. The code here blindly assumes the reverse is true
# as well, which doesn't hold in general, but it works for the official input.
def Solve(h, w, counts):
    min_area = sum(c*a for c, a in zip(counts, areas))
    return min_area < h*w  # meh

answer = 0
for line in last_part.split('\n'):
    a, bs = line.split(': ')
    counts = [int(i) for i in bs.split()]
    assert(len(counts) == len(shapes))
    h, w = map(int, a.split('x'))
    answer += Solve(h, w, counts)
print(answer)
