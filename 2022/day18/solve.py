from math import inf
import sys
import time

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

def SolvePart1(points):
  return sum(q not in points for p in points for q in Neighbors(p))

def SolvePart2(points):
  # Note: this assumes all points on the outer hull are connected!
  sx, sy, sz = min(points)
  sx -= 1

  todo = [(sx, sy, sz)]
  seen = set(todo)
  exterior_area = 0
  for p in todo:
    adj = False
    for q in Neighbors(p):
      if q in points:
        exterior_area += 1
        adj = True
    if adj:
      for q in Neighbors(p):
        if q not in points:
          if q not in seen:
            seen.add(q)
            todo.append(q)
          for r in Neighbors(q):
            if r not in points and r not in seen:
              seen.add(r)
              todo.append(r)
  return exterior_area

def Solve(file):
  points = set(tuple(map(int, line.split(','))) for line in file)
  print(SolvePart1(points))
  print(SolvePart2(points))

if len(sys.argv) > 1:
  for filename in sys.argv[1:]:
    start_time = time.time()
    print(filename + ':')
    with open(filename, 'rt') as f:
      Solve(f)
    print('%.3f s' % (time.time() - start_time))
else:
  Solve(sys.stdin)
