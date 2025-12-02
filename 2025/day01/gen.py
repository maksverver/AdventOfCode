from random import randint

N = 1000000
M = 1000000
for _ in range(N // 3):
    # Right biased so the total counter goes up (exceeds 32 bit integer)
    print('LR'[randint(0,2) != 0] + str(randint(1, M)))
for _ in range(N - N // 3):
    # Left biased biased so the total counter goes down (exceeds 32 bit integer)
    print('LR'[randint(0,2) == 0] + str(randint(1, M)))
