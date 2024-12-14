import re
import sys

W, H = 101, 103

PATTERN = re.compile(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$')

robots = [tuple(map(int, PATTERN.match(line).groups())) for line in sys.stdin]

def PositionAt(robot, t):
    px, py, vx, vy = robot
    x = (px + vx*t)%W
    y = (py + vy*t)%H
    return (x, y)

def OverlapAt(t):
    distinct = set(PositionAt(r, t) for r in robots)
    return len(robots) - len(distinct)

# For debugging/visualization
def PrintGrid(t, file=sys.stderr):
    count = [[0]*W for _ in range(H)]
    for r in robots:
        x, y = PositionAt(r, t)
        count[y][x] += 1
    for row in count:
        print(''.join(('.' if i == 0 else str(min(i, 9))) for i in row), file=file)
    print(file=file)

def Part1():
    # Count robots in each quadrant after 100 steps.
    a = b = c = d = 0
    for r in robots:
        x, y = PositionAt(r, 100)
        a += x < W // 2 and y < H // 2
        b += x > W // 2 and y < H // 2
        c += x < W // 2 and y > H // 2
        d += x > W // 2 and y > H // 2
    return a * b * c * d

def Part2():
    # Turns out the solution occurs at the time where 0 robots overlap.
    # Probably the test case was generated by manually drawing this picture,
    # then letting all robots move off in a different direction.
    t = 0
    while OverlapAt(t) > 0:
        t += 1
    #PrintGrid(t)  # uncomment to see the christmas tree!
    return t

print(Part1())
print(Part2())
