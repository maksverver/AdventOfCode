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

def Encode(r, c):
  return ((r + 0x80000000) << 32) | (c + 0x80000000)

def Decode(i):
  return ((i >> 32) - 0x80000000, (i & 0xffffffff) - 0x80000000)

def Solve():
  rope = [[0, 0] for _ in range(10)]
  visited1 = set([Encode(0, 0)])
  visited2 = set([Encode(0, 0)])

  def Step(dr, dc):
    nonlocal visited1, visited2
    rope[0][0] += dr
    rope[0][1] += dc

    for i in range(1, 10):
      dr = rope[i - 1][0] - rope[i][0]
      dc = rope[i - 1][1] - rope[i][1]
      if max(abs(dr), abs(dc)) <= 1:
        break
      #if i == 9:
      #  print('?', (dr, dc), (rope[0][0] - rope[i][0], rope[0][1] - rope[i][1]))
      rope[i][0] += Clamp(dr, -1, 1)
      rope[i][1] += Clamp(dc, -1, 1)
      if i == 1:
        # moved1 += 1
        visited1.add(Encode(rope[1][0], rope[1][1]))
      if i == 9:
        # moved2 += 1
        visited2.add(Encode(rope[9][0], rope[9][1]))

  # traveled = 0
  # moved1 = 0
  # moved2 = 0
  for i, (direction, distance) in enumerate(instructions):
    dr, dc = directions[direction]
    #traveled += distance
    for _ in range(distance):
      Step(dr, dc)
    if i % 100000 == 0:
      print('%.2f%% done' % (i / len(instructions)), file=sys.stderr)

  # print('traveled:', traveled, file=sys.stderr)
  # print('moved1:', moved1, file=sys.stderr)
  # print('moved2:', moved2, file=sys.stderr)
  # print('width:',  max(r for (r, c) in map(Decode, visited1)) - min(r for (r, c) in map(Decode, visited1)), file=sys.stderr)
  # print('height:', max(c for (r, c) in map(Decode, visited1)) - min(c for (r, c) in map(Decode, visited1)), file=sys.stderr)
  print(len(visited1))
  print(len(visited2))

Solve()
