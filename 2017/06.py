import sys

def SelectIndex(a):
  i = 0
  for j in range(1, len(a)):
    if a[j] > a[i]:
      i = j
  return i

def Redistribute(a, i):
  n = a[i]
  a[i] = 0
  for j in range(i + 1, i + n + 1):
    a[j%len(a)] += 1

a = [int(s) for s in sys.stdin.readline().split()]
i = 0
seen = dict()
while tuple(a) not in seen:
  seen[tuple(a)] = i
  i += 1
  Redistribute(a, SelectIndex(a))

# Part one: total number of iterations until a cycle occurs.
print(len(seen))

# Part two: length of the cycle.
print(len(seen) - seen[tuple(a)])
