import heapq
import re
import sys

pattern = re.compile(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$')
bots = []
for line in sys.stdin:
    x, y, z, r = map(int, pattern.match(line).groups())
    bots.append(((x, y, z), r))

def Part1():
    (x, y, z), r = max(bots, key=lambda bot: bot[1])
    return sum(
        abs(xx - x) + abs(yy - y) + abs(zz - z) <= r
        for (xx, yy, zz), _ in bots)

def Part2():
    class Region:
        def __init__(self, bounds, bots):
            self.bounds = bounds
            self.bots = bots
            self.key = -len(bots), sum(min(abs(lo), abs(hi)) for (lo, hi) in bounds)

        def __lt__(self, other):
            return self.key < other.key

    def DistanceToCube(v, cube):
        def DistanceToSegment(x, segment):
            lo, hi = segment
            if x < lo:
                return lo - x
            if x > hi:
                return x - hi
            return 0
        return sum(DistanceToSegment(x, segment) for x, segment in zip(v, cube))

    initial_bounds = tuple(
        (min(coords[i] for coords, _ in bots),
         max(coords[i] for coords, _ in bots)) for i in range(3))
    regions = [Region(bounds=initial_bounds, bots=bots)]
    while regions:
        region = heapq.heappop(regions)
        k = max(range(3), key=lambda i: region.bounds[i][1] - region.bounds[i][0])
        lo, hi = region.bounds[k]
        if lo == hi:
            return sum(lo for lo, hi in region.bounds)
        mid = lo + (hi - lo)//2
        for (new_lo, new_hi) in ((lo, mid), (mid + 1, hi)):
            new_bounds = region.bounds[:k] + ((new_lo, new_hi),) + region.bounds[k + 1:]
            new_bots = [(point, radius) for point, radius in bots if DistanceToCube(point, new_bounds) <= radius]
            heapq.heappush(regions, Region(bounds=new_bounds, bots=new_bots))

print(Part1())
print(Part2())
