import sys

def ParseOp(line):
  opcode, *operands = line.split()
  if opcode == 'noop':
    assert len(operands) == 0
    return 0
  if opcode == 'addx':
    assert len(operands) == 1
    i = int(operands[0])
    assert i != 0
    return i

answer1 = 0
H, W = 6, 40
picture = [['.']*W for _ in range(H)]
t = 0
x = 1
for op in map(ParseOp, sys.stdin):
  for delay in range(1 if op == 0 else 2):
    r, c = t // W, t % W
    if x - 1 <= c <= x + 1:
      picture[r][c] = '#'
    t += 1
    if t % 40 == 20:
      answer1 += t * x
  x += op
assert t == H * W
print(answer1)
for row in picture:
  print(''.join(row))
