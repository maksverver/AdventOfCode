import sys
from KnotHash import GetLengths, KnotHash, ReduceToHex

def SolvePart1(input):
    lengths = list(map(int, input.split(',')))
    a, b, *_ = KnotHash(lengths, rounds=1)
    return a*b

def SolvePart2(input):
    return ReduceToHex(KnotHash(GetLengths(input)))

input = sys.stdin.readline().strip()
print(SolvePart1(input))
print(SolvePart2(input))
