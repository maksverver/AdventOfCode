import re
import sys

pattern = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$')

class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        assert x1 < x2
        assert y1 < y2
        assert z1 < z2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def Size(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)


def Subtract(c, d):
    '''Subtracts cube `d` from `c` and returns an iterable of disjoint remaining cubes.'''
    if (c.x1 >= d.x2 or c.x2 <= d.x1 or
        c.y1 >= d.y2 or c.y2 <= d.y1 or
        c.z1 >= d.z2 or c.z2 <= d.z1):  # No overlap; keep c
        yield c

    # Check for partial intersection
    elif c.x1 < d.x1 < c.x2:  # Split on x=d.x1
        yield from Subtract(Cube(c.x1, d.x1, c.y1, c.y2, c.z1, c.z2), d)
        yield from Subtract(Cube(d.x1, c.x2, c.y1, c.y2, c.z1, c.z2), d)
    elif c.x1 < d.x2 < c.x2:  # Split on x=d.x2
        yield from Subtract(Cube(c.x1, d.x2, c.y1, c.y2, c.z1, c.z2), d)
        yield from Subtract(Cube(d.x2, c.x2, c.y1, c.y2, c.z1, c.z2), d)
    elif c.y1 < d.y1 < c.y2:  # Split on y=d.y1
        yield from Subtract(Cube(c.x1, c.x2, c.y1, d.y1, c.z1, c.z2), d)
        yield from Subtract(Cube(c.x1, c.x2, d.y1, c.y2, c.z1, c.z2), d)
    elif c.y1 < d.y2 < c.y2:  # Split on y=d.y2
        yield from Subtract(Cube(c.x1, c.x2, c.y1, d.y2, c.z1, c.z2), d)
        yield from Subtract(Cube(c.x1, c.x2, d.y2, c.y2, c.z1, c.z2), d)
    elif c.z1 < d.z1 < c.z2:  # Split on z=d.z1
        yield from Subtract(Cube(c.x1, c.x2, c.y1, c.y2, c.z1, d.z1), d)
        yield from Subtract(Cube(c.x1, c.x2, c.y1, c.y2, d.z1, c.z2), d)
    elif c.z1 < d.z2 < c.z2:  # Split on z=d.z2
        yield from Subtract(Cube(c.x1, c.x2, c.y1, c.y2, c.z1, d.z2), d)
        yield from Subtract(Cube(c.x1, c.x2, c.y1, c.y2, d.z2, c.z2), d)
    else: # c is completely covered by d; drop c
        assert d.x1 <= c.x1 <= c.x2 <= d.x2
        assert d.y1 <= c.y1 <= c.y2 <= d.y2
        assert d.z1 <= c.z1 <= c.z2 <= d.z2


def Solve(steps):
    total_size = 0
    for i, (c, bit) in enumerate(steps):
        if bit == False:
            continue
        cubes = [c]
        for d, _ in steps[i + 1:]:
            cubes = [e for c in cubes for e in Subtract(c, d)]
        total_size += sum(c.Size() for c in cubes)
    return total_size


def Limit(steps):
    '''Limit steps to constraints for Part 1 of the problem.'''
    return [
        (Cube(
            max(c.x1, -50), min(c.x2, 51),
            max(c.y1, -50), min(c.y2, 51),
            max(c.z1, -50), min(c.z2, 51)), bit)
        for c, bit in steps
        if c.x1 <= 51 and c.x2 >= -50 and
           c.y1 <= 51 and c.y2 >= -50 and
           c.z1 <= 51 and c.z2 >= -50]


def ParseLine(line):
    '''Parses a line into tuple: ((x1, x2, y1, y2, z1, z2), bit)'''
    bit, *coords = pattern.match(line).groups()
    x1, x2, y1, y2, z1, z2 = map(int, coords)
    return (Cube(x1, x2 + 1, y1, y2 + 1, z1, z2 + 1), bit == 'on')

steps = [ParseLine(line) for line in sys.stdin]


# Part 1
print(Solve(Limit(steps)))

# part 2
print(Solve(steps))
