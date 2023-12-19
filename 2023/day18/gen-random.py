from itertools import accumulate
from random import randint
import sys

# Output is 16N + 4 lines long.

# Small test set
#N = 555

# Medium test set
N = 1111

# Large test set
#N = 5555

def GenCompact():
  p = []
  corner = 10
  # Without touching:
  #x, y = 3, 3
  #w, h = 2, 2
  # With touching:
  x, y = 3, 2
  w, h = 1, 2
  p.append(('R', corner))
  #rf=0
  rf = 0.5  # randomness
  for c in range(N):
    n = x*min(c + 1, N - c)
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if c > 0:
      p.append(('R', 1))
    p.append(('D', n))
    p.append(('R', w))
    p.append(('U', n))
  p.append(('R', corner))
  p.append(('D', corner))
  for r in range(N):
    n = y*min(r + 1, N - r)
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if r > 0:
      p.append(('D', 1))
    p.append(('L', n))
    p.append(('D', h))
    p.append(('R', n))
  p.append(('D', corner))
  p.append(('L', corner))
  for c in range(N):
    n = x*min(c + 1, N - c)
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if c > 0: p.append(('L', 1))
    p.append(('U', n))
    p.append(('L', w))
    p.append(('D', n))
  p.append(('L', corner))
  p.append(('U', corner))
  for r in range(N):
    n = y*min(r + 1, N - r)
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if r > 0: p.append(('U', 1))
    p.append(('R', n))
    p.append(('U', h))
    p.append(('L', n))
  p.append(('U', corner))
  return p

def GenLarge():
  p = []
  corner = 10
  p.append(('R', corner))

  max_size = 2**20 - 1

  hor_sizes = [randint(2, max_size) for _ in range(2*N - 1)]
  ver_sizes = [randint(2, max_size) for _ in range(2*N - 1)]

  hor_sum = sum(hor_sizes)
  ver_sum = sum(ver_sizes)

  hor_acc = list(accumulate(hor_sizes, initial=0))
  ver_acc = list(accumulate(ver_sizes, initial=0))

  rf = 0.5  # randomness

  for c in range(N):
    n = max(1, min(hor_acc[2*c], hor_sum - hor_acc[2*c + 1], max_size))
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if c > 0:
      p.append(('R', hor_sizes[2*c - 1]))
    p.append(('D', n))
    p.append(('R', hor_sizes[2*c]))
    p.append(('U', n))
  p.append(('R', corner))
  p.append(('D', corner))
  for r in range(N):
    n = max(1, min(ver_acc[2*r], ver_sum - ver_acc[2*r + 1], max_size))
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if r > 0:
      p.append(('D', ver_sizes[2*r - 1]))
    p.append(('L', n))
    p.append(('D', ver_sizes[2*r]))
    p.append(('R', n))
  p.append(('D', corner))
  p.append(('L', corner))
  for c in range(N):
    n = max(1, min(hor_acc[2*c], hor_sum - hor_acc[2*c + 1], max_size))
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if c > 0: p.append(('L', hor_sizes[2*c - 1]))
    p.append(('U', n))
    p.append(('L', hor_sizes[2*c]))
    p.append(('D', n))
  p.append(('L', corner))
  p.append(('U', corner))
  for r in range(N):
    n = max(1, min(ver_acc[2*r], ver_sum - ver_acc[2*r + 1], max_size))
    if rf: n = randint(max(1, int((1 - rf)*n)), n)
    if r > 0: p.append(('U', ver_sizes[2*r - 1]))
    p.append(('R', n))
    p.append(('U', ver_sizes[2*r]))
    p.append(('L', n))
  p.append(('U', corner))
  return p

def Output1(p):
  for d, n in p:
    print(d, n, '(#000000)')

def Output2(p, q):
  assert len(p) == len(q)
  for (d1, n1), (d2, n2) in zip(p, q):
    assert 0 < n2 < 2**20
    print(d1, n1, '(#%06x)' % (n2 * 16 + 'RDLU'.index(d2)))

Output2(GenCompact(), list(reversed(GenLarge())))

