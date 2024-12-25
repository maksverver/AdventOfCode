import sys

locks = []
keys = []

for part in sys.stdin.read().strip().split('\n\n'):
    rows = part.split('\n')
    profile = tuple(c.count('#') for c in zip(*rows))

    if part[0] == '#':
        locks.append(profile)
    else:
        assert part[0] == '.'
        keys.append(profile)

print(sum(all(i + j <= 7 for (i, j) in zip(lock, key)) for lock in locks for key in keys))
