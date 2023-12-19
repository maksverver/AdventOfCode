from random import choice, random, randint, randrange, sample, shuffle
import sys

def BoundsEmpty(bounds):
  return any(hi <= lo for lo, hi in bounds)

def Volume(bounds):
  ans = 1
  for lo, hi in bounds:
    if lo < hi:
      ans *= hi - lo
  return ans

def IntersectBounds(a, b):
  assert len(a) == len(b) == 4
  return [(max(a_lo, b_lo), min(a_hi, b_hi)) for ((a_lo, a_hi), (b_lo, b_hi)) in zip(a, b)]

def IntersectBoundsLists(la, lb):
  return [intersection for a in la for b in lb if not BoundsEmpty(intersection := IntersectBounds(a, b))]

def ComputeWithToplogicalSort():
  num_deps = {'A': 0, 'R': 0}
  rdeps = {'A': [], 'R': []}
  for state in rules:
    num_deps[state] = 2
    rdeps[state] = []
  for state, (f, t, lt, ge) in rules.items():
    rdeps[lt].append(state)
    rdeps[ge].append(state)

  todo = []
  todo.append('A')
  todo.append('R')
  order = []
  while todo:
    for state in rdeps[todo.pop()]:
      assert num_deps[state] > 0
      num_deps[state] -= 1
      if num_deps[state] == 0:
        order.append(state)
        todo.append(state)
  assert all(count == 0 for (state, count) in num_deps.items())

  state_bounds = {'A': [[(1, 4001)]*4], 'R': []}
  for state in order:
    f, t, lt, ge = rules[state]
    lt_bounds = [(1, 4001) if i != f else (1, t)    for i in range(4)]
    ge_bounds = [(1, 4001) if i != f else (t, 4001) for i in range(4)]
    state_bounds[state] = (
        IntersectBoundsLists([lt_bounds], state_bounds[lt]) +
        IntersectBoundsLists([ge_bounds], state_bounds[ge]))
    print(state, state_bounds[state])
  print(sum(map(Volume, state_bounds['in'])))

def PickCondition(bounds_list):
  if not bounds_list:
    return (randrange(0, 4), randint(1, 4000))
  bounds = choice(bounds_list)
  assert not BoundsEmpty(bounds)
  field = randrange(0, 4)
  lo, hi = bounds[field]

  # if random() < 0.01: return randint(1, lo)
  # if random() < 0.01: return randint(hi, 4000)

  return (field, randint(lo, hi))


def SplitOn(bounds_list, field, treshold):
  a = []
  b = []
  for bounds in bounds_list:
    lo, hi = bounds[field]
    if treshold <= lo:
      b.append(bounds)
    elif hi <= treshold:
      a.append(bounds)
    else:
      assert lo < treshold < hi
      a.append(bounds[:field] + [(lo, treshold)] + bounds[field+1:])
      b.append(bounds[:field] + [(treshold, hi)] + bounds[field+1:])
  return (a, b)

def IsInBounds(bounds, fields):
  assert len(bounds) == len(fields) == 4
  return all(lo <= x < hi for (lo, hi), x in zip(bounds, fields))

def IsInBoundsList(bounds_list, fields):
  return any(IsInBounds(bounds, fields) for bounds in bounds_list)


def IndexToName(i):
  k = 1
  n = 27
  while i >= n:
    n += 27*n
    k += 1
  res = ''
  for _ in range(k):
    res = chr(ord('a') + i % 26) + res
    i //= 26
  assert i < 27
  if i > 0: res = chr(ord('a') + i - 1) + res
  return res

N = M = 500       # small
#N = M = 25000     # medium

A = N
R = N + 1
max_outdegree = 10

transitions = [[] for _ in range(N + 2)]
state_bounds = [None]*(N + 2)
state_bounds[R] = []
state_bounds[A] = [[(1, 4001)]*4]

num_nonempty = 0
num_empty = 0

for idx in reversed(range(N)):
  size  = randint(2, min(max_outdegree, N - idx  + 1))
  nexts = sample(population=range(idx + 1, N + 2), k=size)

  accepting_bounds = []
  remaining_bounds = [[(1, 4001)]*4]

  for nxt in nexts[:-1]:
    next_bounds = state_bounds[nxt]
    if remaining_bounds:
      f, t = PickCondition(next_bounds)
    else:
      # Random back-edge on case that is always false
      nxt = randint(0, nxt - 1)
      f, t = PickCondition([])
    a, b = SplitOn(remaining_bounds, f, t)

    op = '<'
    if t > 1 and randint(0, 1) == 1:
      op = '>'
      t = t - 1
      a, b = b, a
    if b:
      num_nonempty += 1
    else:
      num_empty += 1
    accepting_bounds.extend(IntersectBoundsLists(a, next_bounds))
    remaining_bounds = b
    transitions[idx].append((f, t, op, nxt))
  next = nexts[-1]
  accepting_bounds.extend(IntersectBoundsLists(remaining_bounds, state_bounds[next]))
  transitions[idx].append(next)
  state_bounds[idx] = accepting_bounds
#  print(idx, size, nexts, transitions[idx])



print('empty:', num_empty, file=sys.stderr)
print('nonempty:', num_nonempty, file=sys.stderr)

state_names = [IndexToName(i) for i in range(N+2)]
state_names[A] = 'A'
state_names[R] = 'R'
try:
  in_pos = state_names.index('in')
  state_names[0], state_names[in_pos] = state_names[in_pos], state_names[0]
except ValueError:
  state_names[0] = 'in'
assert state_names.count('in') == 1

lines = []
for idx in range(N):
  line = state_names[idx] + '{'
  for f, t, op, nxt in transitions[idx][:-1]:
    line += 'xmas'[f] + op + str(t) + ':' + state_names[nxt] + ','
  line += state_names[transitions[idx][-1]] + '}'
  lines.append(line)
shuffle(lines)
for line in lines:
  print(line)

#print(state_bounds[0], file=sys.stderr)
answer2 = sum(map(Volume, state_bounds[0]))

# Part 1
print()
num_accepted = 0
num_rejected = 0
answer1 = 0
for _ in range(M):
  fields = [randint(1, 4000) for _ in range(4)]
  if IsInBoundsList(state_bounds[0], fields):
    num_accepted += 1
    answer1 += sum(fields)
  else:
    num_rejected += 1
  print('{x=%d,m=%d,a=%d,s=%d}' % tuple(fields))

print('accepted:', num_accepted, file=sys.stderr)
print('rejected:', num_rejected, file=sys.stderr)

print('answer 1:', answer1, file=sys.stderr)
print('answer 2:', answer2, file=sys.stderr)
