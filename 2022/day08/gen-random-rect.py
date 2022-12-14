from random import randint

W = 123
H = 456

for r in range(H):
  print(''.join(str(randint(0, 9)) for _ in range(W)))
