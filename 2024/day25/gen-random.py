from random import randint

def RandomProfile():
    return [randint(0, 5) for _ in range(5)]

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

for i in range(1000000):
    if i > 0:
        print()
    if randint(0, 1) == 0:
        PrintLock(RandomProfile())
    else:
        PrintKey(RandomProfile())
