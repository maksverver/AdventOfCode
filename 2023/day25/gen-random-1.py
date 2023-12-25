# Construction: a cycle of cliques of size 6, connected to each other by
# three edges between consecutive cliques, except for two connections with have
# only 1 and 2 edges respectively. These form the minimum cut.
#
#
#                     component 2
#                |-----------------------------------|
#
#  ----                     ----        ----                    ----
#  ----  clique ---- clique ---- clique ---- clique ---- clique ---- etc.
#  ----         ----        ----        ----                    ----
#

from random import randint, randrange, sample, shuffle
import sys

def Id(n):
  assert n >= 0
  s = ''
  for _ in range(id_len):
    s = chr(ord('a') + n % 26) + s
    n //= 26
  assert n == 0
  return s

edges = []

# Small input
# id_len = 3
# cliques = 2929    #  26**3 // 6

# Large input
id_len = 4
cliques = 76162   #  26**4 // 6

V = cliques * 6

# Place 1/2 edges randomly around the circle. The two components tend to have
# similar size.
# only_one, only_two = sample(range(cliques), k=2)

# Place 1/2 edges together, so we get a one large component and one component
# that consists of only 1 vertex. This is much harder to solve for my
# randomized algorithm.
only_one = randint(0, cliques - 1)
only_two = only_one + 1


for n in range(cliques):
  for i in range(6):
    for j in range(i + 1, 6):
      edges.append((6*n + i, 6*n + j))

  m = (n + 1) % cliques

  if n == only_one:
    k = 1
  elif n == only_two:
    k = 2
  else:
    k = 3

  for i in range(k):
    edges.append((6*n + 3 + i, 6*m + i))


ids = [Id(n) for n in range(V)]
shuffle(ids)
shuffle(edges)

adj = [[] for _ in range(V)]
for v, w in edges:
  if randint(0, 1):
    adj[v].append(w)
  else:
    adj[w].append(v)

for v, ws in enumerate(adj):
  if ws:
    print(ids[v] + ': ' + ' '.join(ids[w] for w in ws))
  # else:
  #   print('empty', file=sys.stderr)

# Calculate expected answer
size1 = (only_one - only_two) % cliques * 6
size2 = (only_two - only_one) % cliques * 6
assert size1 + size2 == V
print(size1 * size2, file=sys.stderr)
