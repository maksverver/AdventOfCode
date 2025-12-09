import sys

def find(commands):
  direction = 0
  distances = [0,0,0,0]
  visited = {(0,0)}
  for command in commands:
    direction = (direction + {'L': 1, 'R': -1}[command[0]])%4
    for _ in range(int(command[1:])):
      distances[direction] += 1
      x, y = distances[0] - distances[2], distances[1] - distances[3]
      if (x, y) in visited:
        return abs(x) + abs(y)
      visited.add((x, y))

print(find(s.strip() for s in sys.stdin.readline().split(',')))
