from collections import defaultdict
import re
import sys

contents = defaultdict(list)     # outer_kind -> [(count, inner_kind)]
container = defaultdict(list)    # inner_kind -> [outer_kind]
content_size_cache = {}          # kind -> total bag count

def ParseInput(file):
    for line in file:
        m = re.match('(\w+ \w+) bags contain ((\d+ \w+ \w+ bags?,? ?)*)', line)
        v = m.group(1)
        for n, w in re.findall('(\d+) (\w+ \w+) bags?', m.group(2)):
            contents[v].append((int(n), w))
            container[w].append(v)

def FindContainers(kind):
    containers = set([])
    todo = [kind]
    for v in todo:
        for u in container[v]:
            if u not in containers:
                containers.add(u)
                todo.append(u)
    return containers

def GetContentSize(kind):
    if kind not in content_size_cache:
        # This assumes there are no cycles!
        content_size_cache[kind] = sum((GetContentSize(k) + 1) * n for (n, k) in contents[kind])
    return content_size_cache[kind]

ParseInput(sys.stdin)
print(len(FindContainers('shiny gold')))    # Part 1
print(GetContentSize('shiny gold'))         # Part 2
