import sys

# Really cool greedy solution.
#
# Runs in O(n) except for the string concatenation.
def Solve(row, k):
    best = row[-k:]
    i = 0
    for ch in reversed(row[:-k]):
        if ch >= best[0]:
            while i + 1 < k and best[i] >= best[i + 1]:
                i += 1
            best = ch + best[:i] + best[i+1:]
    return best

grid = sys.stdin.read().splitlines()

for k in (2, 12):
    print(sum(int(Solve(row, k)) for row in grid))
