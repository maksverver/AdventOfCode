import sys
I = set(int(line.translate({70:48,66:49,76:48,82:49}), 2) for line in sys.stdin)
print(max(I), *(i for i in range(min(I), max(I)) if i not in I))
