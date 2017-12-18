import sys

def Solve(K, N):
    buffer = [0]
    pos = 0
    for _ in range(N):
        pos = (pos + K)%len(buffer)
        buffer = buffer[:pos + 1] + [len(buffer)] + buffer[pos + 1:]
        pos = (pos + 1)%len(buffer)
    return buffer[(pos + 1)%len(buffer)]

print(Solve(int(sys.stdin.readline()), 2017))
