#!/usr/bin/env python3

from random import shuffle, uniform
import sys

def GenHollowCube(r):
  s = set()
  for i in range(-r, r + 1):
    for j in range(-r, r + 1):
      s.add((r, i, j))
      s.add((i, r, j))
      s.add((i, j, r))
      s.add((-r, i, j))
      s.add((i, -r, j))
      s.add((i, j, -r))
  return s

def NestedCubes():
  points = set()
  for r in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19):
    points.update(GenHollowCube(r))
  # Ensure cubes are connected
  for i in range(2, 19):
    points.add((0, 0, i))
  return points

def MengerSponge(depth):
  m = set([(1, 1, 1)])
  for _ in range(depth - 1):
    n = set()
    for x, y, z in m:
      for i in range(3):
        for j in range(3):
          for k in range(3):
            if (i == 1) + (j == 1) + (k == 1) <= 1:
              n.add((3*x - i, 3*y - j, 3*z - k))
    m = n
  return m

def CheckerBoard(size):
  points = set()
  for x in range(size):
    for y in range(size):
      for z in range(size):
        if (x + y + z) % 2 == 0:
          points.add((x, y, z))
  return points

def RandomSphere(r, p):
  points = set()
  for x in range(-r, r):
    for y in range(-r, r):
      for z in range(-r, r):
        if x*x + y*y + z*z < r*r and uniform(0, 1) < p:
          points.add((x, y, z))
  return points

def SpokedCube(inner, outer):
  # Cube with long spokes coming out of it
  points = GenHollowCube(inner)
  for i in range(inner, outer):
    points.add(( i,  0,  0))
    points.add((-i,  0,  0))
    points.add(( 0,  i,  0))
    points.add(( 0, -i,  0))
    points.add(( 0,  0,  i))
    points.add(( 0,  0, -i))
  return points

def OpenCube(inner, outer):
  # Cube of cubes! Lots of hollow space
  # cube with cubes at the edges?
  points = set()
  for i in range(2):
    for j in range(2):
      for k in range(2):
        for x, y, z in GenHollowCube(inner):
          points.add((x + i*outer, y + j*outer, z + k*outer))

  # Connect them all (12 edges of the cubes)
  for i in range(inner + 1, outer - inner):
    for j in range(2):
      for k in range(2):
        points.add(( i,  j*outer, k*outer))
        points.add(( j*outer, i,  k*outer))
        points.add(( j*outer, k*outer,  i))
  return points

def Save(points, output):
  print(output)
  assert isinstance(points, set)  # already deduped
  points = list(points)
  min_x = min(x for x, y, z in points)
  min_y = min(y for x, y, z in points)
  min_z = min(z for x, y, z in points)
  shuffle(points)
  with open(output, 'wt') as f:
    for x, y, z in points:
      print('%d,%d,%d' % (x - min_x, y - min_y, z - min_z), file=f)

# Note: of these, only large-5 is randomly generated

Save(OpenCube(2, 10), 'test.txt')
#Save(NestedCubes(), 'large-1.txt')
#Save(SpokedCube(5, 100), 'large-2.txt')
#Save(MengerSponge(5), 'large-3.txt')
#Save(CheckerBoard(100), 'large-4.txt')
#Save(RandomSphere(50, 0.75), 'large-5.txt')
#Save(OpenCube(5, 100), 'large-6.txt')
#Save(SpokedCube(10, 5000), 'large-7.txt')
#Save(OpenCube(10, 5000), 'large-8.txt')

# Maybe: case with disconnected parts? Not clear if the problem statement allows this.
