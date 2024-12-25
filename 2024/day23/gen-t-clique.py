# Generates a complete graph of all 26 vertices starting with 't',
# which contains 26*25/2 = 325 edges and 26*25*24/3/2/1 = 2600 triangles
# (the answer to part 1).
# 
# This is useful to detect double counting.

from random import shuffle

edges = [
    ['t' + chr(ord('a') + i),
     't' + chr(ord('a') + j)]
    for i in range(26)
    for j in range(i + 1, 26)
]

shuffle(edges)

for edge in edges:
    shuffle(edge)
    print('-'.join(edge))
