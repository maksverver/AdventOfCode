from collections import defaultdict
import re
import sys

# Parse input. We'll assume the x's are positive and y's are negative.
pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
x1, x2, y1, y2 = map(int, pattern.match(sys.stdin.readline()).groups())
x1, x2 = min(x1, x2), max(x1, x2)
assert 0 <= x1
y1, y2 = min(y1, y2), max(y1, y2)
assert y1 <= 0

# For each point in time `t`, start_vx[t] is the list of starting velocities
# in the x direction such that the probe will be between x1 and x2 at time t.
# And similarly for start_vy[t] but in the y direction.
vxs = defaultdict(list)  # t -> [start_vx]
vys = defaultdict(list)  # t -> [start_vy]

# Maximum time possible for the probe to be at y1 or above. Puts an upper bound
# on the number of steps we need to simulate.
max_t = -2*y1 + 1

# Populate vxs.
for start_vx in range(x2 + 1):
    t, x, vx = 0, 0, start_vx
    while t <= max_t and x <= x2 and (x >= x1 or vx > 0):
        if x >= x1:
            vxs[t].append(start_vx)
        x += vx
        if vx > 0:
            vx -= 1
        t += 1

# Populate vys.
for start_vy in range(y1, -y1 + 1):
    t, y, vy = 0, 0, start_vy
    while y >= y1:
        assert t <= max_t
        if y <= y2:
            vys[t].append(start_vy)
        y += vy
        vy -= 1
        t += 1


# Set of initial (vx, vy) pairs such that the probe is in range at some point.
# Deduplication is necessary because for some pairs the probe may be in range
# at multiple timepoints.
joined = set((vx, vy) for t in range(max_t + 1) for vx in vxs[t] for vy in vys[t])

def Part1():
    vy = max(vy for (vx, vy) in joined)
    y = 0
    while vy > 0:
        y += vy
        vy -= 1
    return y


def Part2():
    return len(joined)

print(Part1())
print(Part2())
