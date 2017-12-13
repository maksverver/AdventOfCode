import sys

def Part1(input):
    return sum(pos*rng for pos, rng in input if pos % (2*rng - 2) == 0)

def Part2(input):
    delay = 0
    while True:
        for pos, rng in input:
            if (pos + delay) % (2*rng - 2) == 0:
                break
        else:
            break
        delay += 1
    return delay

input = [[int(part) for part in line.strip().split(': ')] for line in sys.stdin]
print(Part1(input))
print(Part2(input))
