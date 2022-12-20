#!/usr/bin/env python3

from math import inf
import re
import sys

pattern = re.compile('^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)\n$')

# Parse input
valve_names = []  # for debugging
valve_ids = {}    # name -> number
valve_rates = []  # [ints]
valve_dests = []  # [name], then [ints]
for i, line in enumerate(sys.stdin):
  src, flow_rate, dests, _ = pattern.match(line).groups()
  assert src not in valve_ids
  valve_names.append(src)  # for debugging
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

V = len(valve_names)

distance = [[inf for _ in range(V)] for _ in range(V)]
for i in range(V):
  for j in valve_dests[i]:
    distance[i][j] = 1
  distance[i][i] = 0
for k in range(V):
  for i in range(V):
    for j in range(V):
      distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

valves_opened = 'AA -> EY -> WD -> BH -> FB -> VZ -> VI -> AD -> LY -> YC -> HY -> OQ -> IF -> JY -> FL'.split(' -> ')

acc_flow = []
time = 0
current_pos = valve_ids['AA']
for valve in valves_opened:
  valve_id = valve_ids[valve]
  d = distance[current_pos][valve_id]
  print('t=%d move to valve %s (distance %d)' % (time, valve, d))
  time += d
  current_pos = valve_id
  flow_rate = valve_rates[valve_ids[valve]]
  if flow_rate > 0:
    start_time = time
    time += 1
    duration = 30 - time
    acc_flow.append(flow_rate * duration)
    print('t=%d open valve %s (flow rate %d × %d minutes = %d)' %
        (start_time, valve, flow_rate, duration, flow_rate * duration))
print('t=%d total flow %s = %d' % (time, ' + '.join(map(str, acc_flow)), sum(acc_flow)))
