import sys

input = tuple(map(int, sys.stdin.readline().strip()))

PATTERN = (0, 1, 0, -1)

def FFT(s, n):
    for _ in range(n):
        s = tuple(
            abs(sum(x * PATTERN[(j + 1) // (i + 1) % 4] for j, x in enumerate(s))) % 10
            for i in range(len(s)))
    return s

print(''.join(map(str, FFT(input, 100)[:8])))
