from random import randint

H, W = 4096, 1023

def Char(r, c):
    if r < H // 2 and c < W // 2:
        # Relatively high chance to generate XMAS
        return 'XMAS'[randint(0, 1)*2 + (r + c)%2]

    if r >= H // 2 and c >= W // 2:
        # Relatively high chance to generate X-MAS in part 2
        if r % 2 == 0:
            return 'MS'[randint(0,1)]
        else:
            return 'A'

    # Random data just to create some variance.
    xmas = 'XMAS'
    rest = 'BCDEFGHIJKLNOPQRTUVWYZ'
    i = randint(0, len(xmas) - 1)
    if i < len(xmas):
        return xmas[i]
    return rest[randint(0, len(rest) - 1)]

for r in range(H):
    row = ''.join(Char(r, c) for c in range(W))
    print(row)
