from math import lcm
import sys
import re

instrs, rest = sys.stdin.read().split('\n\n')

PATTERN = re.compile(r'(.*) = \((.*), (.*)\)')

# Parse input.
edges = {}
for line in rest.splitlines():
  v, l, r = re.match(PATTERN, line).groups()
  assert v not in edges
  edges[v] = (l, r)

# Finds the cycle period from a given starting pos.
#
# The solution relies on a detail of the input data, without which the problem
# would be much harder: for each starting point, there is a single endpoint on
# the cycle, and it is reached after the p-th step. So if we have a cycle length
# of p, then the endpoint is reached at steps: p, 2p, 3p, 4p, etc.
#
# This implementation is more complicated than it could be because I explicitly
# verify that this holds (see the assertion below).
def FindCycle(pos):
  steps = 0
  last_seen = {}
  end_steps = []
  while (pos, steps % len(instrs)) not in last_seen:
    last_seen[pos, steps % len(instrs)] = steps
    if pos.endswith('Z'):
      end_steps.append(steps)
    instr = instrs[steps % len(instrs)]
    assert instr in 'LR'
    pos = edges[pos][instr == 'R']
    steps += 1
  cycle_start  = last_seen[pos, steps % len(instrs)]
  cycle_length = steps - cycle_start
  assert end_steps == [cycle_length]   # important!!!
  return cycle_length

# Part 1
print(FindCycle('AAA'))

# Part 2
print(lcm(*[FindCycle(start) for start in edges if start.endswith('A')]))
