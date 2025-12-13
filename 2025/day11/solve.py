from collections import defaultdict
from functools import cache
import sys

inputs = defaultdict(list)
outputs = defaultdict(list)
for line in sys.stdin:
    src, dsts = line.strip().split(': ')
    dsts = dsts.split()
    outputs[src] = dsts
    for dst in dsts:
        inputs[dst].append(src)

# Reachability
seen = {'out'}
todo = ['out']
for v in todo:
    for u in inputs[v]:
        if u not in seen:
            seen.add(u)
            todo.append(u)

# Update edges; keep only vertices from which 'out' is reachable.
for src, dsts in outputs.items():
    outputs[src] = [dst for dst in dsts if dst in seen]

@cache
def CountPaths1(v='you'):
    if v == 'out':
        return 1
    return sum(CountPaths1(w) for w in outputs[v])

@cache
def CountPaths2(v='svr', dac=False, fft=False):
    if v == 'out':
        return dac and fft
    dac |= v == 'dac'
    fft |= v == 'fft'
    return sum(CountPaths2(w, dac, fft) for w in outputs[v])

print(CountPaths1())
print(CountPaths2())
