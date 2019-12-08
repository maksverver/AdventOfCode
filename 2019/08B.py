import sys

H, W = 6, 25
digits = list(map(int, sys.stdin.readline().strip()))

def GetPixel(r, c):
    for d in digits[r*W + c::H*W]:
        if d != 2:
            return d

for r in range(H):
    print(''.join(".#"[GetPixel(r, c)] for c in range(W)))
