from functools import cmp_to_key
from random import randint
import sys
import json

def Compare(a, b):
  if isinstance(a, int) and isinstance(b, int):
    return a - b

  if isinstance(a, int):
    return Compare([a], b)

  if isinstance(b, int):
    return Compare(a, [b])

  assert isinstance(a, list) and isinstance(b, list)
  for x, y in zip(a, b):
    if c := Compare(x, y):
      return c

  return len(a) - len(b)


# Returns a list of all possible lists with `l` total sublists and `v` integers.
def GenAll(l, v):
  if l == 0:
    assert v == 1
    return [1]

  if l == 1:
    return [[1]*v]

  assert l > 1

  res = []

  def GenElements(a, l, v):
    if l == 0 and v == 0:
      res.append(a)
      return

    for ll in range(l + 1):
      for vv in range(v + 1):
        if ll > 0 or vv == 1:
          for sub in GenAll(ll, vv):
            GenElements(a + [sub], l - ll, v - vv)

  GenElements([], l - 1, v)
  return res

items = []
for ll in range(1, 5):
  for vv in range(5):
    for a in GenAll(ll, vv):
      #print(a)
      items.append(a)

items.sort(key=cmp_to_key(Compare))
for i, item in enumerate(items):
  if i > 0:
    if Compare(items[i - 1], items[i]) < 0:
      print()
      for j in range(i):
        assert Compare(items[j], items[i]) < 0
        assert Compare(items[i], items[j]) > 0

  print(len(item), item)

