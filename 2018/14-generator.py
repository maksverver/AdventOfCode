# Alternative solution using a generator to produce the sequence of scores.

from itertools import islice
import sys

def Generate():
    scores = [3, 7]
    yield scores[0]
    yield scores[1]
    i = 0
    j = 1
    while True:
        x = scores[i] + scores[j]
        if x < 10:
            yield x
            scores.append(x)
        else:
            y = x // 10
            z = x % 10
            yield y
            yield z
            scores.append(y)
            scores.append(z)
        i = (i + 1 + scores[i]) % len(scores)
        j = (j + 1 + scores[j]) % len(scores)

def Part1(digits):
    pos = int(digits)
    return ''.join(map(str, islice(Generate(), pos, pos + 10)))

def Part2(digits):
    target = int(digits)
    modulus = 10**len(digits)
    current = 0
    for i, x in enumerate(Generate()):
        if current == target:
            return i - len(digits)
        current = (10*current + x) % modulus

digits = sys.stdin.readline().strip()
print(Part1(digits))
print(Part2(digits))
