from random import randint, randrange, sample, shuffle

TOTAL_PROFILES=6**5

def DecodeProfile(i):
    res = []
    for _ in range(5):
        res.append(i % 6)
        i //= 6
    return res

def EncodeProfile(profile):
    i = 0
    for h in reversed(profile):
        i = 6*i + h
    return i

def PrintLock(profile):
    print('#'*len(profile))
    for r in range(5):
        print(''.join('.#'[r < h] for h in profile))
    print('.'*len(profile))

def PrintKey(profile):
    print('.'*len(profile))
    for r in reversed(range(5)):
        print(''.join('.#'[r < h] for h in profile))
    print('#'*len(profile))

for i in range(TOTAL_PROFILES):
    assert EncodeProfile(DecodeProfile(i)) == i

assert TOTAL_PROFILES == 7776
keys  = sample(range(TOTAL_PROFILES), k=5000)
locks = sample(range(TOTAL_PROFILES), k=5000)
outputs = [(PrintLock, lock) for lock in locks] + [(PrintKey, key) for key in keys]
shuffle(outputs)

first = True
for i, (f, a) in enumerate(outputs):
    if i > 0: print()
    f(DecodeProfile(a))
