from collections import deque
from functools import reduce
from operator import mul
import sys

# Dictionary of state transitions in a canonical format. Each transition is a
# single tuple:
#
# (field index, threshold, next state if less, next state if greater or equal)
#
# See ParseRules() below for an example.
rules = {}

# Returns an unordered list of parsed rules.
#
# For example, "a{x<50:b,s>100:c,d}" translates to:
#
#   [ ("a",  (0, 50, "b", "a1")),
#     ("a1", (3, 101, "d", "c")) ]
#
# Assumes: rule names are alphabetic only (so we can construct subrules by
# appending integers), rule names are distinct, and each rule has at least one
# condition (which is true in the official input).
def ParseRules(line):
  rules = []
  name, rest = line.split('{')
  assert name.isalpha()
  assert rest.endswith('}')
  words = rest[:-1].split(',')
  next_state = words[-1]
  assert next_state.isalpha()
  for i, word in reversed(list(enumerate(words[:-1]))):
    state = name if i == 0 else name + str(i)
    cond, state_if_true = word.split(':')
    field = 'xmas'.index(cond[0])
    threshold = int(cond[2:])
    if cond[1] == '<':
      rule = (field, threshold, state_if_true, next_state)
    else:
      assert cond[1] == '>'
      rule = (field, threshold + 1, next_state, state_if_true)
    rules.append((state, rule))
    next_state = state
  assert next_state == name  # triggers if rule has no conditions
  return rules


# Parses a line like "{x=1,m=2,a=3,s=4}" into a list [1, 2, 3, 4].
def ParseItem(line):
  assert line.startswith('{')
  assert line.endswith('}')
  fields = []
  for i, word in enumerate(line[1:-1].split(',')):
    key, val = word.split('=')
    assert key == 'xmas'[i]
    fields.append(int(val))
  return fields


# Parse input
rules, items = sys.stdin.read().strip().split('\n\n')
rules = dict(entry for line in rules.split('\n') for entry in ParseRules(line))
items = list(map(ParseItem, items.split('\n')))


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
    #print(state, state_bounds[state])
  print(sum(map(Volume, state_bounds['in'])))

ComputeWithToplogicalSort()
