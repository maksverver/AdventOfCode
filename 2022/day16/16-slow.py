from math import inf
import re
import sys

pattern = re.compile('^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)\n$')

# Parse input
valve_names = [] # debug
valve_ids = {}    # name -> number
valve_rates = []  # [ints]
valve_dests = []  # [name], then [ints]
for i, line in enumerate(sys.stdin):
  src, flow_rate, dests, _ = pattern.match(line).groups()
  assert src not in valve_ids
  valve_names.append(src) # debug
  valve_ids[src] = i
  valve_rates.append(int(flow_rate))
  dests = dests.split(', ')
  #assert ('tunnels lead to valves ' if len(dests) > 1 else 'tunnel leads to valve ') in line
  valve_dests.append(dests)

# Translate destinations to ids
for dests in valve_dests:
  for i, name in enumerate(dests):
    dests[i] = valve_ids[name]

# We start at valve AA.
start_src = valve_ids['AA']

T = 30

def Search():
  max_flow = -1
  seen = set()
  todo = []

  def Add(time, src, opened, flow):
    nonlocal max_flow
    max_flow = max(max_flow, flow)
    if time < T:
      state = (time, src, opened, flow)
      if state not in seen:
        seen.add(state)
        todo.append(state)

  Add(0, 0, 0, 0)

  for (time, src, opened, flow) in todo:
    if valve_rates[src] > 0 and (opened & (1 << src)) == 0:
      Add(time + 1, src, opened | (1 << src), flow + (T - time - 1) * valve_rates[src])
    for dest in valve_dests[src]:
      Add(time + 1, dest, opened, flow)

  return max_flow

print(Search())
