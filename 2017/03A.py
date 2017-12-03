import sys

N = int(sys.stdin.readline())

def IndexToCoords(n):
  assert n > 0
  if n == 1:
    return (0, 0)
  i, j = n - 2, 1
  while True:
    if i < 2*j:
      return j, -(j - 1) + i
    if i < 4*j:
      return (j - 1) - (i - 2*j), j
    if i < 6*j:
      return -j, (j - 1) - (i - 4*j)
    if i < 8*j:
      return -(j - 1) + (i - 6*j), -j
    i -= 8*j
    j += 1

x, y = IndexToCoords(N)
print(abs(x) + abs(y))
