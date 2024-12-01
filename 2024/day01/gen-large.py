from random import shuffle, randint

def GetRandom():
    return randint(100000, 999999)

common = GetRandom()

num_common = num_random = 500000

a = [common]*num_common + [GetRandom() for _ in range(num_random)]
b = [common]*num_common + [GetRandom() for _ in range(num_random)]
shuffle(a)
shuffle(b)
for x, y in zip(a, b):
    print(x, y, sep='   ')
