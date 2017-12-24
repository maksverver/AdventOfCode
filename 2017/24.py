from collections import Counter, defaultdict
import sys

def Add1(result, strength):
    return result + strength

def Add2(result, strength):
    length, total_strength = result
    return (length + 1, total_strength + strength)

def Solve(components, add, default):
    used = [False]*len(components)
    index = defaultdict(lambda: [])
    for i, (a, b) in enumerate(components):
        index[a].append((i, b))
        if a != b:
            index[b].append((i, a))
    def Search(x, y, i):
        used[i] = True
        best = max((Search(y, z, j) for j, z in index[y] if not used[j]), default = default)
        used[i] = False
        return add(best, x + y)
    return max(Search(0, y, i) for (i, y) in index[0])

components = [tuple(map(int, line.strip().split('/'))) for line in sys.stdin]
print(Solve(components, Add1, 0))
print(Solve(components, Add2, (0, 0))[1])
