import re
import sys

s = list('abcdefgh')

def Swap(x, y):
  s[x], s[y] = s[y], s[x]

def SwapLetter(x, y):
  i = s.index(x)
  j = s.index(y)
  Swap(i, j)

def RotateLeft(n):
  global s
  n %= len(s)
  s = s[n:] + s[:n]

def RotateRight(n):
  RotateLeft(-n)

def RotateLetter(c):
  i = s.index(c)
  RotateRight(i + 1 + (i >= 4))

def Reverse(x, y):
  global s
  assert x < y
  s = s[:x] + list(reversed(s[x:y+1])) + s[y+1:]

def Move(x, y):
  global s
  c = s[x]
  s = s[:x] + s[x+1:]
  s = s[:y] + [c] + s[y:]

def Match(pattern):
  global m, line
  m = re.match(pattern, line)
  return m

for line in sys.stdin:
  if Match(r'swap position (\d+) with position (\d+)'):
    Swap(*map(int, m.groups()))
  elif Match(r'swap letter (\w) with letter (\w)'):
    SwapLetter(*m.groups())
  elif Match(r'rotate left (\d) step'):
    RotateLeft(*map(int, m.groups()))
  elif Match(r'rotate right (\d) step'):
    RotateRight(*map(int, m.groups()))
  elif Match(r'rotate based on position of letter (\w)'):
    RotateLetter(*m.groups())
  elif Match(r'reverse positions (\d+) through (\d+)'):
    Reverse(*map(int, m.groups()))
  elif Match(r'move position (\d+) to position (\d+)'):
    Move(*map(int, m.groups()))
  else:
    assert False
print ''.join(s)
