from heapq import heappush, heappop
import sys

def Memoize(f):
    unset = object()
    memo = {}
    def Memoized(*args):
        value = memo.get(args, unset)
        if value is unset:
            memo[args] = value = f(*args)
        return value
    return Memoized

@Memoize
def GeoIndex(r, c):
    if (r == 0 and c == 0) or (r == Tr and c == Tc):
        return 0
    if r == 0:
        return 16807 * c
    if c == 0:
        return 48271 * r
    return ErosionLevel(r, c - 1) * ErosionLevel(r - 1, c)

@Memoize
def ErosionLevel(r, c):
    return (GeoIndex(r, c) + depth) % 20183

@Memoize
def GeoType(r, c):
    return ErosionLevel(r, c) % 3

def Part1():
    return sum(GeoType(r, c) for r in range(Tr + 1) for c in range(Tc + 1))

def Part2():
    # Tools: NEITHER (0), TORCH (1), GEAR (2)
    # Terrain: ROCKY (0), WET (1), NARROW (2)
    # Then tool x is allowed on terrain y iff. x != y.
    start = ((0, 0), 1)
    finish = ((Tr, Tc), 1)
    todo = []
    dist = {}
    def Update(state, d):
        dd = dist.get(state, -1)
        if dd == -1 or dd > d:
            dist[state] = d
            heappush(todo, (d, state))
    Update(start, 0)
    while todo:
        d, state = heappop(todo)
        if d > dist[state]:
            continue
        if state == finish:
            return d
        (r, c), t = state
        Update(((r, c), 3 - t - GeoType(r, c)), d + 7)
        for rr, cc in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
            if rr >= 0 and cc >= 0 and GeoType(rr, cc) != t:
                Update(((rr, cc), t), d + 1)

line1 = sys.stdin.readline()
line2 = sys.stdin.readline()
assert line1.startswith('depth: ')
depth = int(line1[len('depth: '):])
assert line2.startswith('target: ')
Tc, Tr = map(int, line2[len('target: '):].split(','))

print(Part1())
print(Part2())
