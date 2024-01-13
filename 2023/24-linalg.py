# Advent of Code 2023 Day 24: Never Tell Me The Odds
# https://adventofcode.com/2023/day/24

from fractions import Fraction
from math import inf, gcd, lcm
import sys


def ParseRay(line):
  (x, y, z), (vx, vy, vz) = map(lambda s: map(int, s.split(', ')), line.split(' @ '))
  return ((x, y, z), (vx, vy, vz))


# Read input
rays = [ParseRay(line.strip()) for line in sys.stdin]
N = len(rays)


def Sign(x):
  return (x > 0) - (x < 0)


# Determines whether the rays r and s, when considering their x and y components
# only, have an intersection point (x, y) so that min_x ≤ x ≤ max_x and
# min_y ≤ y ≤ max_y.
#
# This is a typical 2D line intersection algorithm, modified to use integer
# arithmetic only, and to just return True or False based on whether the lines
# intersect and the intersection is in the given window.
#
def CountIntersection2D(r, s, min_x, min_y, max_x, max_y):
  (x1, y1, _), (vx1, vy1, _) = r
  (x2, y2, _), (vx2, vy2, _) = s

  det = vx2 * vy1 - vx1 * vy2
  if det == 0: return 0  # lines are parallel

  dx = x2 - x1
  dy = y2 - y1

  f = vx2 * dy - vy2 * dx  # f/det = position of intersection on r
  g = vx1 * dy - vy1 * dx  # g/det = position of intersection on s

  assert f != 0
  assert g != 0

  if g * Sign(det) < 0: return 0  # collision happened in the past
  if f * Sign(det) < 0: return 0  # collision happened in the past

  if det < 0:
    min_x, max_x = max_x, min_x
    min_y, max_y = max_y, min_y

  return ((min_x*det <= x1*det + vx1*f <= max_x*det) and
          (min_y*det <= y1*det + vy1*f <= max_y*det))


# Part 1
answer1 = 0
for i, r in enumerate(rays):
  for s in rays[i + 1:]:
    min_x = min_y = 200000000000000
    max_x = max_y = 400000000000000
    answer1 += CountIntersection2D(r, s, min_x, min_y, max_x, max_y)
print(answer1)

# Solves a matrix representing a system of N linear equations in augmented
# normal form using Gaus-Jorden elimination. `matrix` must have N rows and
# N + 1 columns.
def SolveMatrix(matrix):
  N = len(matrix)
  assert all(len(row) == N + 1 for row in matrix)

  for i in range(N):
    # Find row j that is nonzero in column i, then swap it to row i.
    j = i
    while matrix[j][i] == 0: j += 1
    matrix[i], matrix[j] = matrix[j], matrix[i]

    # Normalize row so its first nonzero value is 1.
    x = matrix[i][i]
    for c in range(i, N + 1):
      matrix[i][c] /= x

    # Subtract i-th row from other rows, so the only nonzero value in the
    # column is in row i.
    for r in range(N):
      if r != i:
        v = matrix[r][i]
        if v != 0:
          for c in range(i, N + 1):
            matrix[r][c] -= v*matrix[i][c]

  return [row[N] for row in matrix]


# Part 2: solve in a 2D plane (e.g. X/Y) by rewriting it as a system of 4 linear
# equations with 4 unknown variables, yielding x, y, vx, vy of the stone thrown,
# then solve again in a second plane (e.g. X/Z) to also find z and vz.
#
# We use fractions instead of floating point numbers to avoid loss of precision.
#
# Equations stolen from:
# https://github.com/bakkerjangert/AoC_2023/blob/fcc44a084d6b433049fcd6359681703d5abc1674/Day%2024/Day%2024.py#L72-L121
matrix_xy = []
matrix_xz = []
for i in range(4):
    j = i + 1
    (xi, yi, zi), (vxi, vyi, vzi) = rays[i]
    (xj, yj, zj), (vxj, vyj, vzj) = rays[j]
    matrix_xy.append(list(map(Fraction, [vyj - vyi, vxi - vxj, yi - yj, xj - xi, yi * vxi - xi * vyi - yj * vxj + xj * vyj])))
    matrix_xz.append(list(map(Fraction, [vzj - vzi, vxi - vxj, zi - zj, xj - xi, zi * vxi - xi * vzi - zj * vxj + xj * vzj])))

x, y, vx, vy = SolveMatrix(matrix_xy)
w, z, vw, zx = SolveMatrix(matrix_xz)
assert x == w and vx == vw
print(x + y + z)
