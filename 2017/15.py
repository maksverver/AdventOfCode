import sys

MASK = (1 << 16) - 1
MOD = 2147483647
SEED_A = int(sys.stdin.readline().lstrip('Generator A starts with'))
SEED_B = int(sys.stdin.readline().lstrip('Generator B starts with'))

def Generate(value, multiply, modulo, multiples=1):
    while True:
        value = (value*multiply)%modulo
        if value%multiples == 0:
            yield value

def CountMatches(multiples_a, multiples_b, iterations):
    a = Generate(SEED_A, 16807, MOD, multiples_a)
    b = Generate(SEED_B, 48271, MOD, multiples_b)
    return sum(next(a) & MASK == next(b) & MASK for _ in range(iterations))

print(CountMatches(multiples_a=1, multiples_b=1, iterations=40000000))
print(CountMatches(multiples_a=4, multiples_b=8, iterations=5000000))
