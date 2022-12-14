#!/usr/bin/env python

from math import *
from random import *
import sys

max_mod = 2**31 - 1

case = 1

if case == 1:
  max_add = 99
  max_mul = 7
  M = 50
  I = 1000  # (20 per monkey)

if case == 2:
  max_add = 99
  max_mul = 999999999
  M = 500    # monkeys
  I = 10000  # items (20 per monkey)

#M = 5
#I = 15

def ShuffledDistinct(N):
  '''Returns a shuffled list with numbers between 0 and N (exclusive),
  while guaranteeing that the item at index i is not i.
  e.g., for N=3, the result can be [1,2,0] but not [1,0,2]'''
  # This probably doesn't give a proper uniform random answer :/
  assert N > 1
  a = list(range(N))
  shuffle(a)
  i = 0
  while True:
    while a[i] != i:
      i += 1
      if i == N:
        return a
    if i == N - 1:
      a[i - 1], a[i] = a[i], a[i - 1]
      return a
    b = a[i:]
    shuffle(b)
    a = a[:i] + b
  return a

def Product(iterable):
  res = 1
  for i in iterable:
    res *= i
  return res


# Generate graph. All monkeys should be used at least once as a destination.
# Forward distances should be kept small-ish to ensure items are passed around
# multiple times per round. Monkeys can't pass to themselves.
#
# Note that `positive` outcomes are relatively rare, while `negative` outcomes
# are frequent.
pos = ShuffledDistinct(M)
#neg_dists = choices(range(1, M), k=M, weights=[1/(i**2) for i in range(1, M)])
#neg = [(i + d) % M for i, d in enumerate(neg_dists)]
neg = ShuffledDistinct(M)
assert all(i != j for i, j in enumerate(pos))
assert all(i != j for i, j in enumerate(neg))
assert len(set(pos)) == len(pos)  # all monkeys reachable through positive outcomes

candidates = [2, 5, 7, 11, 13, 17, 31] # omits 3, 19, 23
primes = []
while True:
  p = choice(candidates)
  if p*Product(primes) > max_mod:
    break
  primes.append(p)
while 2*Product(primes) <= max_mod:
  primes.append(2)
assert Product(primes) <= max_mod
print(primes, file=sys.stderr)
div = [primes[i % len(primes)] * Product(sample([p for j, p in enumerate(primes) if j != i % len(primes)], k=randint(0,2))) for i in range(M)]
#div = [Product(sample([p for j, p in enumerate(primes)], k=randint(1,3))) for i in range(M)]
mod = lcm(*div)
assert Product(div) > 2**64
assert max_mod // 2 <= mod <= max_mod


items = [[] for _ in range(M)]
for i, c in enumerate(choices(range(M), k=I)):
  #if i < 3:
    # Include three items larger than mod just to mess with people
  #  i = randint(mod, mod + 100)
  items[c].append(i)
assert sum(map(len, items)) == I

updates = []
for i in range(M):
  if randint(0, 3) == 0:
    arg = 'old' if randint(0, 16) == 0 else str(randint(0, max_add))
    updates.append('new = old + ' + arg)
  else:
    # I'm being nice by not multiplying with values such that x * mod > 2**63
    arg = 'old' if (31337 * i) % M == 0 else str(randint(1, max_mul))
    updates.append('new = old * ' + arg)

for i in range(M):
  if i > 0:
    print()
  print('Monkey {}:'.format(i))
  print('  Starting items: {}'.format(', '.join(map(str, items[i]))))
  print('  Operation: {}'.format(updates[i]))
  print('  Test: divisible by {}'.format(div[i]))
  print('    If true: throw to monkey {}'.format(pos[i]))
  print('    If false: throw to monkey {}'.format(neg[i]))

# large-1: part 1 does not overflow 32-bit integer
# large-2: part 2 does overflow 32-bit integer
