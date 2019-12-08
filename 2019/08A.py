from collections import Counter
import sys

H, W = 6, 25
digits = list(map(int, sys.stdin.readline().strip()))
assert len(digits) % (H*W) == 0
counters = [Counter(digits[i:i + H*W]) for i in range(0, len(digits), H*W)]
min_counter = min(counters, key=lambda c: c[0])
print(min_counter[1] * min_counter[2])
