# Generates a replicated pattern of the form:
#
#  0123210
#  1232321
#  2321232
#  3210123
#  2321232
#  1232321
#  0123210
#
# Expect running from 0 up to 9 instead of 3.

def CharAt(r, c):
    r %= 18
    c %= 18
    return str(min(r + c, (18 - r) + c, r + (18 - c), (18 - r) + (18 - c), abs(r - 9) + abs(c - 9)))

H=37*18 + 1
W=57*18 + 1

for r in range(H):
    print(''.join(CharAt(r, c) for c in range(W)))
