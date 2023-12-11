import sys

g = [(x,y) for y,r in enumerate(sys.stdin)
           for x,c in enumerate(r) if c == '#']

for l in 2, 1_000_000:
    print(sum(
        i in ps or l
        for ps in zip(*g)
        for a in ps
        for b in ps
        for i in range(a, b)))

