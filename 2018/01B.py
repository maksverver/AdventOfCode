import sys

def Solve(deltas):
    seen = set()
    freq = 0
    while True:
        for delta in deltas:
            if freq in seen:
                return freq
            seen.add(freq)
            freq += delta

print(Solve([int(s) for s in  sys.stdin]))
