from collections import deque
import re
import sys

class Node:
  pass

nodes = []
for line in sys.stdin:
  m = re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T', line)
  if m:
    node = Node()
    node.x, node.y, node.size, node.used, node.avail = map(int, m.groups())
    nodes.append(node)

min_size = min(node.size for node in nodes)
width = max(node.x for node in nodes) + 1
height = max(node.y for node in nodes) + 1

grid = [['.']*width for _ in range(height)]
for node in nodes:
  if node.used == 0:
    grid[node.y][node.x] = '_'
  elif node.used > min_size:
    grid[node.y][node.x] = '#'
  else:
    grid[node.y][node.x] = '.'

grid[0][0] = 'O'
grid[0][width - 1] = 'G'

# The rest of the solution uses some specific properties of the given test data.
# If we run the following code:
#
#for row in grid:
#  print ''.join(row)
#
# We'd see the grid configuration looks like this:
#
# O...................................G
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# ..............#######################
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# ..................................._.
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
#
# To solve the problem we first need to move '_' to 'G' (moving 'G' leftward),
# then we can continue to move G with a sequence of moves like:
#
#  ..G_.  ->  ..G..  ->  ..G.. -> ..G.. -> ._G.. -> .G_..
#  .....      ..._.      .._..    ._...    .....    .....
#
# Which the above diagram shows takes 5 moves for every space G moves. So the
# answer is just the distance from '_' to 'G' and then 5 times the remaining
# distance between O and G.

# Breadth-first search for the distances from '_' to 'G':
def InitialDist():
  start, = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '_']
  dist = {start: 0}
  todo = deque([start])
  while todo:
    r, c = todo.popleft()
    if grid[r][c] == 'G':
      return dist[r, c]
    for r2, c2 in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
      if 0 <= r2 < height and 0 <= c2 < width and grid[r2][c2] != '#' and (r2, c2) not in dist:
        dist[r2, c2] = dist[r, c] + 1
        todo.append((r2, c2))

print(InitialDist() + 5*(width - 2))
