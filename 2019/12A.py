from functools import reduce
from math import gcd
import re
import sys

class Moon:
    def __init__(self, p, v):
        self.p = tuple(p)
        self.v = tuple(v)

    def Update(self, moons):
        v = tuple(
                self.v[d] + sum((self.p[d] < moon.p[d]) - (self.p[d] > moon.p[d]) for moon in moons)
                for d in range(3))
        p = tuple(self.p[d] + v[d] for d in range(3))
        return Moon(p, v)

    def Energy(self):
        return sum(map(abs, self.p)) * sum(map(abs, self.v))

    def AsTuple(self):
        return self.p + self.v

    def __hash__(self):
        return hash(self.AsTuple())

    def __eq__(self, other):
        return other.__class__ == Moon and self.AsTuple() == other.AsTuple()

    def __repr__(self):
        return 'Moon(p=(%d, %d, %d), v=(%d, %d, %d))' % self.AsTuple()

def Step(moons):
    return tuple(moon.Update(moons) for moon in moons)

def ParseLine(line):
    return Moon(map(int, re.match('<x=(.*), y=(.*), z=(.*)>', line).groups()), (0, 0, 0))

moons = tuple(map(ParseLine, sys.stdin))
for _ in range(1000):
    moons = Step(moons)
print(sum(moon.Energy() for moon in moons))
