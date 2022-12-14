from random import choices

W = 1000
H = 1000

for r in range(H):
  row = []
  for c in range(W):
    d = min(min(r, c), min(H - 1 - r, W - 1 - c))
    max_h = min(9, d // (min(H, W) // 40))
    h, = choices(list(range(max_h + 1)), weights=list(1.5**-i for i in range(max_h + 1)), k=1)
    row.append(h)
  print(''.join(map(str, row)))
