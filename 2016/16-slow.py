import sys

def Generate(s, n):
  while len(s) < n:
    s = s + '0' + ''.join('01'[c == '0'] for c in reversed(s))
  return s[:n]

def Checksum(s):
  while len(s)%2 == 0:
    s = ''.join('01'[s[i] == s[i + 1]] for i in range(0, len(s), 2))
  return s

input = sys.stdin.readline().strip()
print(Checksum(Generate(input, 272)))
print(Checksum(Generate(input, 35651584)))
