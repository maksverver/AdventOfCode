from random import randint

opts = '....>v'
H = 1000
W = 1000
for _ in range(H):
    line = ''.join(opts[randint(0, len(opts) - 1)] for _ in range(W))
    print(line)
