from intcode import RunMachine
import sys

ints = list(map(int, sys.stdin.readline().split(',')))

def Probe(x, y):
    result, = RunMachine(ints, (x, y))
    return result

def FindSquare(size):
    s1 = size - 1
    y = 10   # random starting point where the beam is continuous
    x1 = 0
    while not Probe(x1, y):
        x1 += 1
    x2 = x1 + 1
    while Probe(x2, y):
        x2 += 1
    window = [0]*s1
    while window[y % s1] - x1 < size:
        window[y % s1] = x2
        y += 1
        while not Probe(x1, y):
            x1 += 1
        while Probe(x2, y):
            x2 += 1
    return x1, y - s1

# Part 1
print(sum(Probe(x, y) for x in range(50) for y in range(50)))

# Part 2
x, y = FindSquare(100)
print(x * 10000 + y)
