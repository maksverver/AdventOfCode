import sys

rolls = {(r, c): ch
        for r, line in enumerate(sys.stdin)
        for c, ch in enumerate(line.strip())}

for part in (1, 2):
    answer = 0
    changed = True
    while changed:
        changed = False
        for v, ch in rolls.items():
            if ch == '@':
                r, c = v
                neighbors = sum(rolls.get(w) == '@' for w in [
                        (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                        (r,     c - 1),             (r,     c + 1),
                        (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)])
                if neighbors < 4:
                    answer += 1
                    if part == 2:
                        rolls[v] = '.'
                        changed = True

    print(answer)
