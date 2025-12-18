# Advent of Code 2025 day 2: Gift Shop (https://adventofcode.com/2025/day/2)
#
# Fast solution that works for arbitrarily large inputs.
#
# Inspired by:
#
#  - https://old.reddit.com/r/adventofcode/comments/1pcbgai/2025_day_2_day_2_should_be_easy_right_closed/
#  - https://github.com/janjitse/advent-of-code-2025/blob/master/src/day02.rs

from math import floor, log10, sqrt
import sys

def CountDigits(i):
    '''Returns the number of digits in the decimal representation of the nonnegative integer i.'''
    if i == 0: return 1
    return floor(log10(i)) + 1

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

def Moebius(n):
    '''Returns (-1)**k if `n` is the product of `k` distinct primes,
    or 0 if `n` divisible by any square.'''
    assert n >= 1
    sign = 1
    for p in primes:
        if p*p > n:
            break
        if n % p == 0:
            n //= p
            sign = -sign
            if n % p == 0:
                return 0
    return -sign if n > 1 else sign

def CountBetween(lo, hi, rep):
    '''Returns the count of numbers between `lo` and `hi` (inclusive)
        which are periodic with a number of repetitions that is
        equal to or a multiple of `rep`.'''
    min_digits = (CountDigits(lo) + (rep - 1)) // rep
    max_digits = CountDigits(hi) // rep
    count = 0
    for digits in range(min_digits, max_digits + 1):
        pattern = sum(10**(i*digits) for i in range(rep))
        a = max(10**(digits - 1), (lo + pattern - 1) // pattern)
        b = min(10**(digits) - 1, hi // pattern)
        if a > b: break
        #assert sum(range(a, b + 1)) * 2 == b*b + b - a*a + a
        count += (b*b + b - a*a + a)//2 * pattern
    return count

def ParseRange(s):
    lo, hi = map(int, s.split('-'))
    return (lo, hi)

ranges = [ParseRange(part) for part in sys.stdin.read().strip().split(',')]
max_hi = max(hi for _, hi in ranges)
primes = Primes(floor(sqrt(max_hi)))

def Solve(rep):
    return sum(CountBetween(lo, hi, rep) for lo, hi in ranges)

def Part1():
    return Solve(2)

def Part2():
    return sum(Solve(rep) * sign
            for rep in range(2, CountDigits(max_hi) + 1)
            if (sign := -Moebius(rep)) != 0)

print(Part1())
print(Part2())
