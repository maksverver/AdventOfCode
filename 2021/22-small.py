import re
import sys

pattern = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')

def ParseLine(line):
    bit, *coords = pattern.match(line).groups()
    return (tuple(map(int, coords)), bit == 'on')

steps = [ParseLine(line) for line in sys.stdin]

def Part1():
    cubes = set()
    for (x1, x2, y1, y2, z1, z2), bit in steps:
        for x in range(max(x1, -50), min(x2, 50) + 1):
            for y in range(max(y1, -50), min(y2, 50) + 1):
                for z in range(max(z1, -50), min(z2, 50) + 1):
                    if bit:
                        cubes.add((x, y, z))
                    else:
                        cubes.discard((x, y, z))
    return len(cubes)

print(Part1())

