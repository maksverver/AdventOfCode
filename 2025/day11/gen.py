import sys
from random import shuffle, sample, randint, choice

reserved = {'out', 'you', 'svr', 'dac', 'fft'}
chars = 'abcdefghijklmnopqrstuvwxyz'
names = [name for name in [x + y + z for x in chars for y in chars for z in chars] if name not in reserved]
shuffle(names)

print(len(names), file=sys.stderr)
outputs: dict[str, list[str]] = {}

add_cycles = True
C1 = 100
C2 = 99

N = len(names) - (C1 + C2 if add_cycles else 0)
X = 3000
M = 10

nodes = ['out']
dist = {'out': 0}
for i in range(N):
    if i == N - 1:
        v = 'svr'
    else:
        v = names.pop()
    outputs[v] = sample(nodes[-X:], k=min(X, len(nodes), randint(1, M)))
    dist[v] = 1 + min(dist[w] for w in outputs[v])
    nodes.append(v)

path = ['svr']
while path[-1] != 'out':
    v = path[-1]
    path.append(next(w for w in outputs[v] if dist[w] < dist[v]))

you = path[len(path) * 3 // 4]
dac = path[len(path) * 2 // 4]
fft = path[len(path) * 1 // 4]
substitutions = {
    you: 'you',
    dac: 'dac',
    fft: 'fft',
}

print([substitutions.get(v, v) for v in path], file=sys.stderr)

if add_cycles:
    # Add two cycles.
    #
    # Cycle 1 is reachable from many parts of the graph, but 'out' is not
    # reachable from it. Cycle 2 is not reachable from the graph, but it
    # has many outputs in the graph.
    cycle1 = [names.pop() for _ in range(C1)]
    cycle2 = [names.pop() for _ in range(C2)]
    for i in range(len(cycle1)): outputs[cycle1[i-1]] = [cycle1[i]]
    for i in range(len(cycle2)): outputs[cycle2[i-1]] = [cycle2[i]]
    for node in sample(nodes[1:], N // 10): outputs[node].append(choice(cycle1))
    #for node in sample(nodes[1:], N // 10): outputs[choice(cycle2)].append(node)

srcs = list(outputs.keys())
shuffle(srcs)
for src in srcs:
    print(substitutions.get(src, src) + ': ' +
            ' '.join(substitutions.get(dst, dst) for dst in outputs[src]))
