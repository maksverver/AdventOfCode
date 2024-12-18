from random import shuffle

H = W = 501  # medium
#H = W = 2501  # large
points = [(r, c) for r in range(H) for c in range(W) if (r, c) not in ((0, 0), ((H-1), (W-1)))]
shuffle(points)
for r, c in points:
    print(c, r, sep=',')
