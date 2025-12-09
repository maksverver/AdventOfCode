import sys

commands = [s.strip() for s in sys.stdin.readline().split(',')]

direction = 0
distances = [0,0,0,0]

for command in commands:
  direction = (direction + {'L': 1, 'R': -1}[command[0]])%4
  distances[direction] += int(command[1:])
print(abs(distances[0] - distances[2]) + abs(distances[1] - distances[3]))
