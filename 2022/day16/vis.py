#!/usr/bin/env python3

import re
import sys

pattern = re.compile('^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)\n$')

print('digraph G {')

for line in sys.stdin:
  src, flow_rate, dests, _ = pattern.match(line).groups()
  flow_rate = int(flow_rate)
  dests = dests.split(', ')
  #assert ('tunnels lead to valves ' if len(dests) > 1 else 'tunnel leads to valve ') in line

  print('{} [label="{} ({})" style=filled fillcolor={}]'.format(
      src, src, flow_rate, ("green" if flow_rate > 0 else "white")))
  for dest in dests:
    print('{} -> {}'.format(src, dest))

print('}')

