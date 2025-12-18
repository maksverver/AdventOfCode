from math import floor, log10

def CountDigits(i):
    '''Returns the number of digits in the decimal representation of the nonnegative integer i.'''
    if i == 0: return 1  # not always necessary
    return floor(log10(i)) + 1

def SplitNumber(i):
    '''Splits a number in half, e.g. SplitNumber(1234) == (12, 34)'''
    digits = CountDigits(i)
    assert digits % 2 == 0
    div = 10**(digits // 2)
    return i // div, i % div

def Primes(max):
    '''Returns a list of all prime numbers less than or equal to `max`.'''
    if max < 2:
        return []
    # Find odd primes, using the Sieve of Eratosthenes:
    is_prime = [False] + [True]*((max - 1)//2)
    for i, v in enumerate(is_prime):
        if not v:
            continue
        start = 2*i*i + 2*i
        if start > len(is_prime):
            break
        for j in range(start, len(is_prime), 2*i + 1):
            is_prime[j] = False
    return [2] + [2*i + 1 for i, v in enumerate(is_prime) if v]
