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

for row in grid:
  print ''.join(row)
