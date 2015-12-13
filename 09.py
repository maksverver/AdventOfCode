from collections import defaultdict
import sys

dists = defaultdict(dict)

def Search(path, total_dist, combiner):
    if len(path) == len(dists):
        return total_dist, path
    return combiner(
        Search(
            path + [place],
            total_dist + (dists[path[-1]][place] if path else 0),
            combiner)
        for place in dists if place not in path)

for line in sys.stdin:
    src, _, dst, _, dist = line.split()
    dists[src][dst] = dists[dst][src] = int(dist)

print Search([], 0, min)  # Part 1
print Search([], 0, max)  # Part 2
