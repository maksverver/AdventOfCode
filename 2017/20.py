from collections import defaultdict
import re
import sys

RE = 'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>'

MAX_TIME = 1000  # long enough

class Particle:
    def __init__(self, line):
        self.px, self.py, self.pz, \
        self.vx, self.vy, self.vz, \
        self.ax, self.ay, self.az = map(int, re.match(RE, line).groups())

    def getPosAt(self, t):
        u = t*(t + 1)//2
        qx = self.px + self.vx*t + self.ax*u
        qy = self.py + self.vy*t + self.ay*u
        qz = self.pz + self.vz*t + self.az*u
        return qx, qy, qz

    def getDistAt(self, t):
        x, y, z = self.getPosAt(t)
        return abs(x) + abs(y) + abs(z)

def Part1(particles):
    distances = [p.getDistAt(MAX_TIME) for p in particles]
    return distances.index(min(distances))

def Part2(particles):
    for t in range(MAX_TIME):
        count = defaultdict(lambda: 0)
        for p in particles:
            count[p.getPosAt(t)] += 1
        particles = [p for p in particles if count[p.getPosAt(t)] == 1]
    return len(particles)

particles = [Particle(line) for line in sys.stdin]
print(Part1(particles))
print(Part2(particles))
