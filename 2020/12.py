import sys

class Ship1():
    def __init__(self):
        self.sx, self.sy = 0, 0
        self.dx, self.dy = 1, 0
    def Move(self, dx, dy):
        self.sx += dx
        self.sy += dy
    def Turn(self, turns):
        for _ in range(turns):
            self.dy, self.dx = self.dx, -self.dy
    def Forward(self, dist):
        self.sx += self.dx * dist
        self.sy += self.dy * dist
    def Dist(self):
        return abs(self.sx) + abs(self.sy)

class Ship2(Ship1):
    def __init__(self):
        self.sx, self.sy =  0, 0
        self.dx, self.dy = 10, 1
    def Move(self, dx, dy):
        self.dx += dx
        self.dy += dy

def AngleToTurns(a):
    assert a % 90 == 0
    return a // 90 % 4

def Execute(instructions, ship):
    for (cmd, dist) in instructions:
        if cmd == 'N': ship.Move(0, dist)
        elif cmd == 'E': ship.Move(dist, 0)
        elif cmd == 'S': ship.Move(0, -dist)
        elif cmd == 'W': ship.Move(-dist, 0)
        elif cmd == 'L': ship.Turn(AngleToTurns(dist))
        elif cmd == 'R': ship.Turn(AngleToTurns(-dist))
        elif cmd == 'F': ship.Forward(dist)
        #print(cmd, dist, (ship.sx, ship.sy), (ship.dx, ship.dy))
    return ship

instructions = [(line[0], int(line[1:])) for line in sys.stdin]
print(Execute(instructions, Ship1()).Dist())
print(Execute(instructions, Ship2()).Dist())
