# Source: https://gathering.tweakers.net/forum/list_message/77606444#77606444

import collections as C


G = C.defaultdict(set)

for line in open(0):
    u, *vs = line.replace(':','').split()
    for v in vs: G[u].add(v); G[v].add(u)


S = set(G)

count = lambda v: len(G[v]-S)

while sum(map(count, S)) != 3:
    S.remove(max(S, key=count))

print(len(S) * len(set(G)-S))
