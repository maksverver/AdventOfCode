from functools import reduce
from operator import xor

def Reverse(l, pos, length):
    for k in range(length//2):
        i = (pos + k)%len(l)
        j = (pos + length - 1 - k)%len(l)
        l[i], l[j] = l[j], l[i]

def GetLengths(input):
    return list(map(ord, input)) + [17, 31, 73, 47, 23]

def KnotHash(lengths, rounds = 64):
    l = list(range(256))
    pos = 0
    skip = 0
    for _ in range(rounds):
        for length in lengths:
            Reverse(l, pos, length)
            pos += length + skip
            skip += 1
    return l

def ReduceToHex(l):
    return ''.join('%02x'%reduce(xor, l[i:i + 16]) for i in range(0, 256, 16))

def ReduceToInt(l):
    result = 0
    for i in range(0, 256, 16):
        result = (result << 8) | reduce(xor, l[i:i + 16])
    return result
