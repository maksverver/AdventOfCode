from math import inf
import sys

points = set()

for line in sys.stdin:
  x, y, z = map(int, line.split(','))
  points.add((x, y, z))

def Neighbors(p):
  x, y, z = p
  return [
    (x + 1, y, z),
    (x - 1, y, z),
    (x, y + 1, z),
    (x, y - 1, z),
    (x, y, z + 1),
    (x, y, z - 1),
  ]

def SolvePart1():
  return sum(q not in points for p in points for q in Neighbors(p))

def SolvePart2():
  # Determine outside bounds of the volume
  min_x = min_y = min_z = inf
  max_x = max_y = max_z = -inf
  for x, y, z in points:
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

  # Flood-fill from the outside:
  todo = (
    [(min_x - 1, y, z) for y in range(min_y, max_y + 1) for z in range(min_z, max_z + 1)] +
    [(max_x + 1, y, z) for y in range(min_y, max_y + 1) for z in range(min_z, max_z + 1)] +
    [(x, min_y - 1, z) for x in range(min_x, max_x + 1) for z in range(min_z, max_z + 1)] +
    [(x, max_y + 1, z) for x in range(min_x, max_x + 1) for z in range(min_z, max_z + 1)] +
    [(x, y, min_z - 1) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)] +
    [(x, y, max_z + 1) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)])
  seen = set(todo)
  exterior_area = 0
  for p in todo:
    for q in Neighbors(p):
      x, y, z = q
      if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
        if q in points:
          exterior_area += 1
        elif q not in seen:
          seen.add(q)
          todo.append(q)
  return exterior_area

print(SolvePart1())
print(SolvePart2())
