import sys

adjacent = {}
visited = set()

def Search(i):
    global visited
    if i in visited:
        return
    visited.add(i)
    for j in adjacent[i]:
        Search(j)

for line in sys.stdin:
    src, dests = line.strip().split(' <-> ')
    adjacent[int(src)] = [int(dest) for dest in dests.split(', ')]

# Part 1
Search(0)
print(len(visited))

# Part 2
groups = 1
for i in adjacent:
    if i in visited:
        continue
    Search(i)
    groups += 1
print(groups)
