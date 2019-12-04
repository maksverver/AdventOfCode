import sys

a, b = map(int, sys.stdin.readline().split('-'))

def Valid(i):
    s = '%06d' % i
    has_double = False
    i = 0
    while i < len(s):
      if i > 0 and s[i] < s[i - 1]:
        return False
      j = i + 1
      while j < len(s) and s[i] == s[j]:
        j += 1
      if j - i == 2:
        has_double = True
      i = j
    return has_double

print(sum(Valid(i) for i in range(a, b + 1)))
