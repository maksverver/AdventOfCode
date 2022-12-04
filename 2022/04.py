import sys

def ParsePair(word):
  return tuple(map(int, word.split('-')))

def ParseLine(line):
  return tuple(map(ParsePair, line.strip().split(',')))

pairs = list(map(ParseLine, sys.stdin))

print(sum(((a <= c and d <= b) or (c <= a and b <= d)) for (a, b), (c, d) in pairs))
print(sum(a <= d and b >= c for (a, b), (c, d) in pairs))
