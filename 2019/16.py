import sys

def FFT(s):
    n = len(s)
    t = [0]*(n + 1)
    for i, x in enumerate(s):
        t[i + 1] = t[i] + x

    def CalcDigit(i):
        x = 0
        j = i
        while j < n:
            x += t[min(j + i + 1, n)] - t[j]
            j += 2*i + 2
            if j >= n:
                break
            x -= t[min(j + i + 1, n)] - t[j]
            j += 2*i + 2
        return abs(x) % 10


    return [CalcDigit(i) for i in range(n)]

def RepeatFFT(s, n):
    for _ in range(n):
        s = FFT(s)
    return s

line = sys.stdin.readline().strip()

signal = tuple(map(int, line))
offset = int(line[:7])

print(''.join(map(str, RepeatFFT(signal, 100)[:8])))
print(''.join(map(str, RepeatFFT(signal * 10000, 100)[offset:offset + 8])))
