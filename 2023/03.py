from collections import defaultdict
import sys

M = [s.strip() for s in sys.stdin]
H = len(M)
W = len(M[0])

def Neighbors(r, c):
  return [(rr, cc)
      for (rr, cc) in [
          (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
          (r,     c - 1),             (r,     c + 1),
          (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
      if 0 <= rr < H and 0 <= cc < W]

def IsSymbol(ch):
  return ch != '.' and not ch.isdigit()

answer1 = 0
symbols = defaultdict(list)  # (r,c) -> [adjacent values]
for r in range(H):
  c = 0
  while c < W:
    value = 0       # number starting at (r, c)
    nearby = set()  # (r, c) of adjacent symbols
    while c < W and M[r][c].isdigit():
      value = 10*value + int(M[r][c])
      for rr, cc in Neighbors(r, c):
        if IsSymbol(M[rr][cc]):
          nearby.add((rr, cc))
      c += 1
    if nearby:
      answer1 += value
      for pos in nearby:
        symbols[pos].append(value)
    c += 1
print(answer1)

answer2 = 0
for (r, c), vals in symbols.items():
  if M[r][c] == '*' and len(vals) == 2:
    answer2 += vals[0] *  vals[1]
print(answer2)
