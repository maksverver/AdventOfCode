import sys

PATTERN = (0, 1, 0, -1)

def FFT(signal, offset):
    n = len(signal)

    # t[i] == sum(signal[0:i])
    t = [0]*(n + 1)
    for i, x in enumerate(signal):
        t[i + 1] = t[i] + x

    result = [0]*n
    width = offset
    for i in range(n):
        x = 0
        j = 0
        while j < n:
            pat_idx = (j + offset) // width % 4
            pat_pos = (j + offset) % width
            pat_len = min(width - pat_pos, n - j)
            x += PATTERN[pat_idx] * (t[j + pat_len] - t[j])
            j += pat_len
        result[i] = abs(x) % 10
        width += 1
    return result

def RepeatFFT(signal, times, offset):
    for _ in range(times):
        signal = FFT(signal, offset)
    return signal

line = sys.stdin.readline().strip()

signal = tuple(map(int, line))
offset = int(line[:7])

print(''.join(map(str, RepeatFFT(signal, times=100, offset=1)[:8])))
print(''.join(map(str, RepeatFFT((signal * 10000)[offset:], times=100, offset=offset+1)[:8])))
