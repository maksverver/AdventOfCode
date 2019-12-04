import sys

a, b = map(int, sys.stdin.readline().split('-'))

def Valid(i):
    s = '%06d' % i
    has_double = False
    for i in range(1, len(s)):
        if int(s[i]) < int(s[i - 1]):
            return False
        if int(s[i]) == int(s[i - 1]):    
            has_double = True
    return has_double

print(sum(Valid(i) for i in range(a, b + 1)))
