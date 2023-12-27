from functools import reduce
import sys

# Parses a brick into a tuple ((x1, y1, x1), (x2, y2, x2)) and normalizes the
# coordinates so that x1 ≤ x2, y1 ≤ y2, z1 ≤ z2.
def ParseBrick(line):
  (x1, y1, z1), (x2, y2, z2) = map(lambda s: map(int, s.split(',')), line.split('~'))
  assert (x1 != x2) + (y1 != y2) + (z1 != z2) <= 1
  if x1 > x2: x2, x1 = x1, x2
  if y1 > y2: y2, y1 = y1, y2
  if z1 > z2: z2, z1 = z1, z2
  return ((x1, y1, z1), (x2, y2, z2))


# Calculates where all bricks will drop, and returns an array `supported_by`
# where `supported_by[i]` is a set of indices of bricks that the i-th brick
# rests upon. Bricks use indices 1 through N, while index 0 is reserved for the
# floor.
#
# This runs in O(N × L) time and produces at most N × L edges, where L is the
# average length of a brick.
#
def CalculateSupport(bricks):
  supported_by = [set()]
  height = {}  # (x, y) -> (h, i)
  for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(bricks, 1):
    s = set()
    max_h = 0
    for x in range(x1, x2 + 1):
      for y in range(y1, y2 + 1):
        h, j = height.get((x, y), (0, 0))
        if h > max_h:
          max_h = h
          s.clear()
        if h == max_h:
          s.add(j)
    new_h = max_h + (z2 - z1 + 1)
    for x in range(x1, x2 + 1):
      for y in range(y1, y2 + 1):
        height[x, y] = new_h, i
    supported_by.append(s)
  return supported_by


def Part1(supported_by):
  # Count the number of blocks that are safe to remove, where a block is safe to
  # remove if all the blocks it supports are supported by at least one other
  # block.
  #
  # This runs in O(N + E) time, where E is the number of edges, i.e., the sum
  # of the sizes of the elements of `supported_by`.
  #
  safe_to_remove = [True]*len(supported_by)
  safe_to_remove[0] = False  # never remove the floor
  for s in supported_by:
    if len(s) == 1: safe_to_remove[min(s)] = False
  return sum(safe_to_remove)


# More efficient solution of part 2 using Lowest Common Ancestors.
#
# Runs in O(V + E log V) time.
#
# Define the parent of a brick i as the highest brick j whose removal would
# cause j to fall, or 0 if there is none. Then if j is not 0, removing j's
# parent would cause j to fall and therefore i too, and so on. The total number
# of bricks that would cause j to fall is exactly the number of ancestors of i
# (i.e, j itself, j's parent, j's parent's parent, etc.)
#
# How do we calculate the parents? If brick i is supported by only a single
# brick j, then j is the parent of i. Otherwise, consider the tree defined by
# the parent relationship (with 0 as the root). Then the parent of i is the
# lowest common ancestor of the bricks that support i (i.e., it is the highest
# single brick that would cause all those bricks to fall).
#
def Part2(supported_by):
  depth  = [0]
  answer = 0
  ancestors = {(0, 0): 0}

  def NthAncestorPowerOf2(x, k):
    res = ancestors.get((x, k))
    if res is None:
      ancestors[x, k] = res = NthAncestorPowerOf2(NthAncestorPowerOf2(x, k - 1), k - 1)
    return res

  def NthAncestor(x, n):
    k = 0
    while (1 << k) <= n:
      if n & (1 << k): x = NthAncestorPowerOf2(x, k)
      k += 1
    return x

  def Parent(x):
    return ancestors[x, 0]

  def LowestCommonAncestor(x, y):
    n = depth[x]
    m = depth[y]
    if n > m: x = NthAncestor(x, n - m)
    if m > n: y = NthAncestor(y, m - n)
    if x == y: return x
    k = 0
    while NthAncestorPowerOf2(x, k) != NthAncestorPowerOf2(y, k):
      k += 1
    while k > 0:
      k -= 1
      a = NthAncestorPowerOf2(x, k)
      b = NthAncestorPowerOf2(y, k)
      if a != b: x, y = a, b
    assert x != y and Parent(x) == Parent(y)
    return Parent(x)

  for i, s in enumerate(supported_by[1:], 1):
    ancestors[i, 0] = lca = reduce(LowestCommonAncestor, s)
    depth.append((d := depth[lca]) + 1)
    answer += d
  return answer


def Main():
  bricks = [ParseBrick(line.strip()) for line in sys.stdin]
  bricks.sort(key=lambda brick: brick[0][2])
  supported_by = CalculateSupport(bricks)
  print(Part1(supported_by))
  print(Part2(supported_by))


if __name__ == '__main__': Main()
