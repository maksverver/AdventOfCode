import sys

directions = {
  'U': (-1,  0),
  'D': (+1,  0),
  'L': ( 0, -1),
  'R': ( 0, +1),
}

def ParseInstruction(line):
  direction, distance = line.split()
  return (direction, int(distance))

instructions = list(map(ParseInstruction, sys.stdin))

def Clamp(x, lo, hi):
  return lo if x < lo else hi if x > hi else x

def Solve(knots):
  rope = [[0, 0] for _ in range(knots)]
  visited = set([(0, 0)])

  def Step(dr, dc):
    rope[0][0] += dr
    rope[0][1] += dc

    for i in range(1, knots):
      dr = rope[i - 1][0] - rope[i][0]
      dc = rope[i - 1][1] - rope[i][1]
      if max(abs(dr), abs(dc)) <= 1:
        break
      rope[i][0] += Clamp(dr, -1, 1)
      rope[i][1] += Clamp(dc, -1, 1)
    else:
      visited.add(tuple(rope[-1]))

  for direction, distance in instructions:
    dr, dc = directions[direction]
    for _ in range(distance):
      Step(dr, dc)

  return len(visited)

print(Solve(2))
print(Solve(10))
