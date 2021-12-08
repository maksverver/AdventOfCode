import itertools
import sys

segments = [
    "abcefg",  # 0
    "cf",      # 1
    "acdeg",   # 2
    "acdfg",   # 3
    "bcdf",    # 4
    "abdfg",   # 5
    "abdefg",  # 6
    "acf",     # 7
    "abcdefg", # 8
    "abcdfg",  # 9
]

displays = []  # list of pairs of list of string (the signals) and list of strings (the digits)
for line in sys.stdin:
    a, b = line.split('|')
    displays.append((a.split(), b.split()))

# Part 1
unique_lengths = [2, 3, 4, 7]
print(sum(len(digit) in unique_lengths for signals, digits in displays for digit in digits))

# Part 2
chars = 'abcdefg'
perms = [''.join(p) for p in itertools.permutations(chars)]

def Permute(signal, perm):
    return ''.join(sorted(chars[perm.index(c)] for c in signal))

def CheckPerm(signals, perm):
    for signal in signals:
        if Permute(signal, perm) not in segments:
            return False
    return True

def FindPermutation(signals):
    signals = sorted(signals, key=len)  # optimization
    perm, = [p for p in itertools.permutations(chars) if CheckPerm(signals, p)]
    return perm

def DecodeDigits(digits, perm):
    value = 0
    for digit in digits:
        value *= 10
        value += segments.index(Permute(digit, perm))
    return value

def Solve(signals, digits):
    return DecodeDigits(digits, FindPermutation(signals))

print(sum(Solve(signals, digits) for signals, digits in displays))
