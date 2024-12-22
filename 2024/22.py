from collections import Counter
import sys

secret_numbers = list(map(int, sys.stdin))

def Next(x):
    x = (x ^ (x <<  6)) & 0xffffff
    x = (x ^ (x >>  5)) & 0xffffff
    x = (x ^ (x << 11)) & 0xffffff
    return x

def Nth(x, n):
    for _ in range(n):
        x = Next(x)
    return x

# Returns a dictionary where each key is a 4-tuple of delta values,
# and the associated value is the first price for that key.
def FirstPricesBySequence(x, n):
    seq = (),
    price_by_seq = {}
    last_price = x % 10
    for _ in range(n):
        x = Next(x)
        price = x % 10
        seq = seq[-3:] + (price - last_price,)
        last_price = price
        if len(seq) == 4 and seq not in price_by_seq:
            price_by_seq[seq] = price
    return price_by_seq

def SolvePart1():
    return sum(Nth(x, 2000) for x in secret_numbers)

def SolvePart2():
    c = Counter()
    for x in secret_numbers:
        c += FirstPricesBySequence(x, 2000)
    return max(c.values())

print(SolvePart1())
print(SolvePart2())
