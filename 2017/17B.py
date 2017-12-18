import sys

def Solve(K, N):
    succ = [0]*(N + 1)
    for i in range(N):
        v = i
        for _ in range(K):
            v = succ[v]
        succ[i + 1] = succ[v]
        succ[v] = i + 1
    return succ[0]

print(Solve(int(sys.stdin.readline()), 50000000))
