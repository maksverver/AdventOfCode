#!/usr/bin/env python

# Converts an input file to DIMACS graph format.
#
# Then the clique can be found with a command line tool like
# cliquer's `cl`. See: https://users.aalto.fi/~pat/cliquer.html
#
# Example usage:
#
#   % ./input-to-dimacs.py ../sampledata/23-sample.in | cl -
#   Reading graph from stdin...OK
#   Searching for a single maximum weight clique...
#   size=4, weight=4:   4 6 7 14
#
#   % ./input-to-dimacs.py ../sampledata/23-sample.in 4 6 7 14
#   co,de,ka,ta

import sys

if len(sys.argv) < 2:
    print('Usage: %s <input>               -- to encode the input as DIMACS' % sys.argv[0])
    print('Usage: %s <input> [<vertex>...] -- to translate vertex ids back to names' % sys.argv[0])
    sys.exit(1)

vertex_names = []
vertex_ids_by_name = {}

def Vertex(s):
    if s not in vertex_ids_by_name:
        vertex_names.append(s)
        vertex_ids_by_name[s] = len(vertex_ids_by_name)
    return vertex_ids_by_name[s]

edges = []

with open(sys.argv[1]) as f:
    for line in f:
        v, w = line.strip().split('-')
        edges.append((Vertex(v) + 1, Vertex(w) + 1))

if len(sys.argv) == 2:
    # Print graph in DIMACS format
    print('p', 'edge', len(vertex_names), len(edges))
    for v, w in edges:
        print('e', v, w)
else:
    # Translate vertex ids back to names
    names = []
    for arg in sys.argv[2:]:
        v = int(arg)
        assert 0 < v <= len(vertex_names)
        names.append(vertex_names[v - 1])
    print(','.join(sorted(names)))
