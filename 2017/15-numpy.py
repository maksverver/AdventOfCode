import numpy as np
import sys

MASK = (1 << 16) - 1
MOD = 2147483647
SEED_A = int(sys.stdin.readline().lstrip('Generator A starts with'))
SEED_B = int(sys.stdin.readline().lstrip('Generator B starts with'))
MULT_A = 16807
MULT_B = 48271

def GenerateMultipliers(multiply, chunk_size):
    '''Returns an array a of length chunk_size such that:
        a[i] == multiply**(i + 1) % MOD'''
    a = np.array([multiply], dtype=np.uint64)
    while len(a) < chunk_size:
        a = np.concatenate([a, a * multiply % MOD])
        multiply = multiply * multiply % MOD
    return a[:chunk_size]

def Part1(iterations, chunk_size=10000):
    multiply_values = np.column_stack([
        GenerateMultipliers(MULT_A, chunk_size),
        GenerateMultipliers(MULT_B, chunk_size)])
    seed = np.array([SEED_A, SEED_B], dtype=np.uint64)
    multiply_seed = np.array(
        [pow(MULT_A, chunk_size, MOD), pow(MULT_B, chunk_size, MOD)],
        dtype=np.uint64)
    assert iterations % chunk_size == 0
    matches = 0
    for _ in range(iterations // chunk_size):
        values = multiply_values * seed % MOD
        seed = seed * multiply_seed % MOD
        truncated_values = values.astype(np.uint16)
        matches += np.sum(truncated_values[:,0] == truncated_values[:,1])
    return matches

def Part2(iterations, chunk_size=10000):
    def Generate(seed, multiply, multiples):
        parts = []
        total = 0
        multiply_seed = pow(multiply, chunk_size, MOD)
        multiply_values = GenerateMultipliers(multiply, chunk_size)
        while total < iterations:
            values = multiply_values * seed % MOD
            seed = seed * multiply_seed % MOD
            truncated = values.astype(np.uint16)
            selected = np.compress(values % multiples == 0, truncated)
            if total + len(selected) > iterations:
                selected = selected[:iterations - total]
            parts.append(selected)
            total += len(selected)
        return np.concatenate(parts)
    a = Generate(SEED_A, MULT_A, 4)
    b = Generate(SEED_B, MULT_B, 8)
    return np.sum(a == b)

print(Part1(iterations=40000000))
print(Part2(iterations=5000000))
