from collections import defaultdict
import sys

contains = defaultdict(list)        # outer_kind -> [(count, inner_kind)]
contained_by = defaultdict(list)    # inner_kind -> [outer_kind]
content_size = {}                   # kind -> total bag count

def ParseInput(file):
    for line in file:
        outer, rest = line.strip('\n.').split(' contain ', 1)
        a, b, c = outer.split()
        assert c == 'bags'
        outer_kind = a + ' ' + b
        if rest != 'no other bags':
            parts = rest.split(', ')
            for part in parts:
                n, a, b, c = part.split(' ')
                assert c in ('bag', 'bags')
                inner_count = int(n)
                inner_kind = a + ' ' + b
                contains[outer_kind].append((inner_count, inner_kind))
                contained_by[inner_kind].append(outer_kind)

def FindContainers(kind):
    containers = set([])
    todo = [kind]
    for v in todo:
        for u in contained_by[v]:
            if u not in containers:
                containers.add(u)
                todo.append(u)
    return containers

def GetContentSize(kind):
    if kind not in content_size:
        # This assumes there are no cycles!
        content_size[kind] = sum((GetContentSize(k) + 1) * n for (n, k) in contains[kind])
    return content_size[kind]

ParseInput(sys.stdin)
print(len(FindContainers('shiny gold')))    # Part 1
print(GetContentSize('shiny gold'))         # Part 2
