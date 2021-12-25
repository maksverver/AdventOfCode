from operator import mul
from functools import reduce
import re
import sys

pattern = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$')


def ParseLine(line):
    bit, *coords = pattern.match(line).groups()
    x1, x2, y1, y2, z1, z2 = map(int, coords)
    return (((x1, x2 + 1), (y1, y2 + 1), (z1, z2 + 1)), bit == 'on')


steps = [ParseLine(line) for line in sys.stdin]


def Subtract(o, p):
    '''Given cuboids `o` and `p` as tuples of (min, max) pairs, returns an
    iterable of disjoint cuboids that remain when subtracting  `q` from `p`.'''
    if any(a >= d or b <= c for (a, b), (c, d) in zip(o, p)):
        # o and p don't overlap, so return o.
        yield o
        return

    for i, ((a, b), (c, d)) in enumerate(zip(o, p)):
        for v in c, d:
            if a < v < b:
                # Split on the i-th dimension
                yield from Subtract(o[:i] + ((a, v),) + o[i + 1:], p)
                yield from Subtract(o[:i] + ((v, b),) + o[i + 1:], p)
                return

    # o is completely covered by p, so drop o.
    assert all(c <= a <= b <= d for (a, b), (c, d) in zip(o, p))


def Product(iterable):
    return reduce(mul, iterable)


def Size(bounds):
    return Product(b - a for a, b in bounds)


def Solve(steps):
    total_size = 0
    for i, (o, bit) in enumerate(steps):
        if bit == False:
            continue
        cuboids = [o]
        for p, _ in steps[i + 1:]:
            cuboids = [q for o in cuboids for q in Subtract(o, p)]
        total_size += sum(Size(p) for p in cuboids)
    return total_size


def Limit(steps):
    '''Limit steps to constraints for Part 1 of the problem.'''
    return [
        (tuple((max(a, -50), min(b, 51)) for a, b in bounds), bit)
        for bounds, bit in steps
        if all(a <= 51 and b >= -50 for a, b in bounds)]


# Part 1
print(Solve(Limit(steps)))

# part 2
print(Solve(steps))
