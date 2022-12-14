from random import *
import json
import sys

min_value = 0
max_value = 100

num_lists  = 100
num_values = 100
num_pairs  = 30000    # must be a multiple of 3

def GenTree(num_lists, num_values, first_value):
  stack = [[]]
  while num_lists or num_values or len(stack) > 1:
    i = randint(0, num_lists + num_values + len(stack) - 2)
    if i < num_lists:
      stack.append([])
      num_lists -= 1
    elif i - num_lists < num_values:
      if first_value is None:
        number = randint(min_value, max_value)
      else:
        number = first_value
        first_value = None
      stack[-1].append(number)
      num_values -= 1
    else:
      stack[-2].append(stack.pop())
  return stack.pop()

def Size(t):
  if isinstance(t, int):
    return 1
  return 1 + sum(map(Size, t))

def Depth(t):
  if isinstance(t, int):
    return 0
  if t == []:
    return 1
  return max(map(Depth, t)) + 1

def Str(t):
  if isinstance(t, int):
    return str(t)
  return '[' + ','.join(map(Str, t)) + ']'

def MutationOf(t):
  mutation_pos = randint(0, Size(t) - 1)
  pos = -1

  def Dfs(t):
    nonlocal pos
    pos += 1
    if pos != mutation_pos:
      # Return a copy
      if isinstance(t, int):
        return t
      else:
        return list(map(Dfs, t))

    else:

      if isinstance(t, int):
        # Change to a different value
        v = randint(min_value, max_value - 1)
        if v == t: v += 1
        return v

      else:
        x = randint(0, len(t) + (len(t) > 1)*2)
        if x < len(t):
          # Delete a random value
          # We don't need to insert because of symmetry between pairs
          u = list(t)
          u.pop(x)
          return u
        x -= len(t)

        if x == 0:
          # Append an empty list
          return t + [[]]
        elif x == 1:
          # Replace with a random element
          assert len(t) > 1
          return choice(t)
        else:
          assert x == 2
          # Wrap in an extra list
          assert len(t) > 1
          return [t]

  return Dfs(t)

def FirstValue(t):
  if isinstance(t, int):
    return t
  for v in map(FirstValue, t):
    if v is not None:
      return v
  return None


sys.setrecursionlimit(10000)
while True:
  t1 = GenTree(num_lists, num_values, 1)
  t2 = GenTree(num_lists, num_values, 4)
  t3 = GenTree(num_lists, num_values, 7)
  values = sorted(map(FirstValue, [t1, t2, t3]))
  if values[0] <= 2 <= values[1] <= 6 <= values[2]:
    break

pairs = []
for t in [t1, t2, t3]:
  for i in range(num_pairs // 3):
    print(i, file=sys.stderr)
    #u = MutationOf(t)
    u = t  # generates lots of duplicates which are slow to sort!
    v = MutationOf(u)
    if randint(0, 1) == 1:
      u, v = v, u
    pairs.append((u, v))
shuffle(pairs)

for i, (u, v) in enumerate(pairs):
  print('%.2f%%' % (i * 100.0 / len(pairs)), file=sys.stderr)
  if i != 0:
    print()
  print(Str(u))
  print(Str(v))
