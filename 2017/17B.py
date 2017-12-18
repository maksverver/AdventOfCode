import sys

def Solve(K, N):
    pos = -1
    for n in range(1, N + 1):
        pos = (pos + 1 + K)%n
        if pos == 0:
            answer = n
    return answer

print(Solve(int(sys.stdin.readline()), 50000000))
