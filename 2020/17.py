import sys

def Neighbors3D(p):
    x, y, z, w = p
    return [(x + dx, y + dy, z + dz, w)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        if dx or dy or dz]

def Neighbors4D(p):
    x, y, z, w = p
    return [(x + dx, y + dy, z + dz, w + dw)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        for dw in (-1, 0, 1)
        if dx or dy or dz or dw]

def Iterate(active, neighbours):
    def CountActiveNeighbors(p):
        return sum(q in active for q in neighbours(p))

    inactive = set(q for p in active for q in neighbours(p) if q not in active)

    return set(
        [p for p in active if CountActiveNeighbors(p) in (2, 3)] +
        [p for p in inactive if CountActiveNeighbors(p) == 3])

def Solve(active, neighbours):
    for _ in range(6):
        active = Iterate(active, neighbours)
    return len(active)

initial_active = set((c, r, 0, 0)
    for r, line in enumerate(sys.stdin)
    for c, ch in enumerate(line.strip())
    if ch == '#')

print(Solve(initial_active, Neighbors3D))
print(Solve(initial_active, Neighbors4D))
