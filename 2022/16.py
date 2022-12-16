from math import inf
import re
import sys

pattern = re.compile('^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(, [A-Z]{2})*)\n$')

# Parse input
valve_ids = {}    # name -> number
valve_rates = []  # [ints]
valve_dests = []  # [name], then [ints]
for i, line in enumerate(sys.stdin):
  src, flow_rate, dests, _ = pattern.match(line).groups()
  assert src not in valve_ids
  valve_ids[src] = i
  valve_rates.append(int(flow_rate))
  dests = dests.split(', ')
  #assert ('tunnels lead to valves ' if len(dests) > 1 else 'tunnel leads to valve ') in line
  valve_dests.append(dests)

# Translate destinations to ids
for dests in valve_dests:
  for i, name in enumerate(dests):
    dests[i] = valve_ids[name]

# Distance matrix between all pairs of valves (Floyd-Warshall)
V = len(valve_ids)
M = [[(0 if i == j else inf) for j in range(V)] for i in range(V)]
for src, dests in enumerate(valve_dests):
  for dest in dests:
    assert src != dest
    M[src][dest] = 1
for k in range(V):
  for i in range(V):
     for j in range(V):
        M[i][j] = min(M[i][j], M[i][k] + M[k][j])

valves_with_flow = [i for i in range(V) if valve_rates[i] != 0]

# Compress distance matrix to only valve with flow
start_src = valve_ids['AA']
start_dist = [M[start_src][v] for v in valves_with_flow]
V = len(valves_with_flow)
M = [[M[v][w] for w in valves_with_flow] for v in valves_with_flow]
F = [valve_rates[v] for v in valves_with_flow]

def CalculateMemo(T):
  memo = [[[0 for _ in range(1 << V)] for _ in range(V)] for _ in range(T + 1)]
  unopened = [[i for i in range(V) if (o & (1 << i)) == 0] for o in range(1 << V)]
  for t in range(1, T + 1):
    for v in range(V):
      for o, u in enumerate(unopened):
        if (o & (1 << v)) == 0: continue
        m = memo[t - 1][v][o]
        for w in u:
          d = M[v][w]
          if d >= t: continue
          m = max(m, memo[t - d - 1][w][o | (1 << w)] + (t - d - 1)*F[w])
        memo[t][v][o] = m
  return memo

memo = CalculateMemo(30)

def MaxRelease(T, preopened):
  res = 0
  for v, d in enumerate(start_dist):
    bit = 1 << v
    if (preopened & bit) == 0 and d < T:
      res = max(res, memo[T - d - 1][v][preopened | bit] + (T - d - 1)*F[v])
  return res

print(MaxRelease(30, 0))

print(max(MaxRelease(26, i) + MaxRelease(26, (1 << V) - 1 - i) for i in range(1 << (V - 1))))

