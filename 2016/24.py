import sys

def Distance(src, dst):
  seen = set([src])
  todo = [(0, src)]
  for dist, (r, c) in todo:
    if (r, c) == dst:
      return dist
    for r2, c2 in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
      if grid[r2][c2] != '#' and (r2, c2) not in seen:
        seen.add((r2, c2))
        todo.append((dist + 1, (r2, c2)))

def ShortestPath(visited, loop):
  prev = visited[-1]
  if len(visited) == len(waypoints):
    return distances[prev, start] if loop else 0
  return min(distances[prev, next] + ShortestPath(visited + [next], loop)
      for next in waypoints if next not in visited)

grid = [line.strip() for line in sys.stdin]

waypoints = []
for r, row in enumerate(grid):
  for c, cell in enumerate(row):
    if cell.isdigit():
      waypoints.append((r, c))
      if cell == '0':
        start = (r, c)

distances = {}
for a in waypoints:
  for b in waypoints:
    if a < b:
      distances[a, b] = distances[b, a] = Distance(a, b)

print(ShortestPath([start], False))  # Part 1
print(ShortestPath([start], True))   # Part 2
