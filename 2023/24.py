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


# Represents a range of evenly-spaced integers between given minimum and
# maximum values (which may be -inf and +inf respectively).
#
# Phrased differently, they are the numbers:
#
#   min_x ≤ base_x + k×multiplier ≤ max_x where k is an arbitrary integer
#
# Internal invariants:
#
#  - 0 <= base_x < multiplier
#  - min_x == -inf or (min_x - base_x) % multiplier == 0
#  - max_x ==  inf or (max_x - base_x) % multiplier == 0
#
class Range:
  def __init__(self, base_x=0, multiplier=1, min_x=-inf, max_x=inf):
    assert multiplier > 0
    assert -inf <= min_x <= max_x <= inf
    assert min_x == -inf or (base_x - min_x) % multiplier == 0
    assert max_x == +inf or (max_x - base_x) % multiplier == 0
    self.base_x = base_x % multiplier
    self.multiplier = multiplier
    self.min_x = min_x
    self.max_x = max_x

  def __repr__(self):
    return f'Range({self.base_x}, {self.multiplier}, {self.min_x}, {self.max_x})'

  def Contains(self, x):
    if x == -inf: return min_x == -inf
    if x ==  inf: return max_x ==  inf
    return min_x <= x <= max_x and (x - base_x) % self.multiplier == 0

  # Returns a range that represents the intersection of this range and another
  # one, or None if the resulting range would be empty.
  def Intersect(self, other):
    b1, m1 = self.base_x, self.multiplier
    b2, m2 = other.base_x, other.multiplier

    assert 0 <= b1 < m1
    assert 0 <= b2 < m2

    if (b2 - b1) % gcd(m1, m2) != 0: return None

    mm = lcm(m1, m2)  # new multiplier
    while b1 != b2:
      if b1 < b2:
        assert b1 < mm
        b1 += m1 * ((b2 - b1) // m1)
        if b1 < b2: b1 += m1
      else:
        assert b2 < b1 < mm
        b2 += m2 * ((b1 - b2) // m2)
        if b2 < b1: b2 += m2
    assert b1 == b2
    base_x = b1
    assert 0 <= base_x < mm

    min_x = max(self.min_x, other.min_x)
    max_x = min(self.max_x, other.max_x)

    if min_x > -inf:
      m = min_x % mm
      if m < base_x: min_x += base_x - m
      elif m > base_x: min_x += base_x - m + mm
      assert min_x % mm == base_x

    if max_x < inf:
      m = max_x % mm
      if m > base_x: max_x += base_x - m
      elif m < base_x: max_x += base_x - m - mm
      assert max_x % mm == base_x

    if min_x > max_x: return None

    return Range(base_x, mm, min_x, max_x)


def TrySlope(slope, dim):
  bounds = []
  for xyz, uvw in rays:
    rx = xyz[dim]
    ru = uvw[dim]
    bounds.append((rx, slope - ru))

  start_x = Range()

  for x, u in bounds:
    if u > 0:
      start_x = start_x.Intersect(Range(x, u, -inf, x))
    elif u < 0:
      start_x = start_x.Intersect(Range(x, -u, x, inf))
    else:
      start_x = start_x.Intersect(Range(x, 1, x, x))
    if start_x is None: return None

  return start_x


# Part 2. We want to determine a ray that intersects with all other rays. We'll
# use the assumption that the input is overconstrained, and solve for each
# dimension individually, calculating a base coordinate and a slope for each
# dimension individually, so that all rays x_i + t*v_i intersect with the
# ray base + slope * t.
#
# This is done by guessing the slope (using values between -1000 and 1000,
# similar to range of velocities used in the input file) and then  calculating
# the possible base values for each slope (see TrySlope() for details).
#
answer2 = 0
for dim in range(3):
  base = None
  for slope in range(-1000, +1000):
    if (r := TrySlope(slope, dim)):
      assert r.min_x == r.max_x  # expect a single answer
      assert base is None # expect exactly one answer per dimension
      base = r.min_x
      answer2 += base

      # Sanity check: for this base and slope, there is a nonnegative integer
      # intersection time for each of the rays
      for xyz, uvw in rays:
        x = xyz[dim]
        u = uvw[dim]
        if x != base:
          assert (base - x) % (u - slope) == 0
          t = (base - x) // (u - slope)
          assert t >= 0

print(answer2)
