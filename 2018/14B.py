import sys

def Solve(digits):
    scores = [3, 7]
    i = 0
    j = 1
    while True:
        x = scores[i] + scores[j]
        for x in (x,) if x < 10 else (x//10, x%10):
            scores.append(x)
            if scores[-len(digits):] == digits:
                return len(scores) - len(digits)
        i = (i + 1 + scores[i]) % len(scores)
        j = (j + 1 + scores[j]) % len(scores)

digits = list(map(int, sys.stdin.readline().strip()))
print(Solve(digits))
