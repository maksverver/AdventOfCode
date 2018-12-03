import sys

ids = list(word.strip() for word in sys.stdin)
for i, a in enumerate(ids):
    for b in ids[:i]:
        common = ''.join(c for (c, d) in zip(a, b) if c == d)
        if len(common) == len(a) - 1 == len(b) - 1:
            print(common)
