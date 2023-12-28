# Advent of Code 2023 Day 19: Aplenty
# https://adventofcode.com/2023/day/19

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


def IsAccepted(item):
  state = 'in'
  while state not in ('A', 'R'):
    f, t, lt, ge = rules[state]
    state = [lt, ge][item[f] >= t]
  return state == 'A'


def CountSolutions(state, bounds):
  if state == 'R':
    return 0

  if state == 'A':
    return reduce(mul, (lo - hi for (lo, hi) in bounds))

  f, t, lt, ge = rules[state]
  lo, hi = bounds[f]

  if t >= hi:
    return CountSolutions(lt, bounds)

  if t <= lo:
    return CountSolutions(ge, bounds)

  return (
    CountSolutions(lt, bounds[:f] + [(lo, t)] + bounds[f+1:]) +
    CountSolutions(ge, bounds[:f] + [(t, hi)] + bounds[f+1:]))


# Parse input
rules, items = sys.stdin.read().strip().split('\n\n')
rules = dict(entry for line in rules.split('\n') for entry in ParseRules(line))
items = list(map(ParseItem, items.split('\n')))

# Solve part 1
print(sum(sum(item) for item in items if IsAccepted(item)))

# Solve part 2
print(CountSolutions('in', [(1, 4001)]*4))
