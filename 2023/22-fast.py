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


bricks = [ParseBrick(line.strip()) for line in sys.stdin]
bricks.sort(key=lambda brick: brick[0][2])

# Calculate where all bricks will drop
#
supported_by = [None for _ in range(len(bricks))]
supporting   = [[] for _ in range(len(bricks))]
height = {}  # (x, y) -> (h, i)
for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(bricks):
  coords = [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
  below = [height[p] for p in coords if p in height]
  max_h = max((h for h, j in below), default=0)
  supported_by[i] = set(j for h, j in below if h == max_h)
  for j in supported_by[i]: supporting[j].append(i)
  new_h = max_h + (z2 - z1 + 1)
  height.update((p, (new_h, i)) for p in coords)


def Part1():
  # Count the number of blocks that are safe to remove, where a block is safe to
  # remove if all the blocks it support are supported by at least one other block.
  safe_to_remove = [True]*len(bricks)
  for s in supported_by:
    if len(s) == 1: safe_to_remove[min(s)] = False
  return sum(safe_to_remove)


# More efficient solution of part 2 using Lowest Common Ancestors.
#
# Define the parent of a brick i as the highest brick j whose removal would
# cause j to fall, or 0 if there is none. Then if j is not 0, j's parent would
# cause j to fall and therefore i too, and so on. The total number of bricks
# that would cause j to fall is exactly the number of ancestors of i (i.e, j,
# j's parent, j's parent's parent, etc.)
#
# How do we calculate the parents? If brick i is supported by only a single
# brick j, then j is the parent of i. Otherwise, consider the tree defined by
# the parent relationship (with 0 as the root). Then the parent of i is the
# lowest common ancestor of the bricks that support i (i.e., it is the highest
# single brick that would cause all those bricks to fall).
#
# The current algorithm runs in O(N log^2 N) time. This can be optimized to
# O(N log N) by reduction to range minimum query but I'm too lazy to do it.
def Part2():
  # Reserve index 0 for the root. Note this means we need to add 1 to all
  # brick indices (i, j, k) below, which is slightly tricky.
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

  def LowestCommonAncestor(x, y):
    n = depth[x]
    m = depth[y]
    if n > m: x = NthAncestor(x, n - m)
    if m > n: y = NthAncestor(y, m - n)
    lo, hi = 0, min(n, m)
    while lo < hi:
      mid = (lo + hi) // 2
      if NthAncestor(x, mid) != NthAncestor(y, mid):
        lo = mid + 1
      else:
        hi = mid
    assert NthAncestor(x, lo) == NthAncestor(y, lo) and (
          lo == 0 or NthAncestor(x, lo - 1) != NthAncestor(y, lo - 1))
    return NthAncestor(x, lo)

  for i, s in enumerate(supported_by):
    if not s:
      lca = 0  # Resting directly on the floor
    else:
      j, *rest = s
      lca = j + 1
      for k in rest:
        lca = LowestCommonAncestor(lca, k + 1)

    ancestors[i + 1, 0] = lca
    depth.append(depth[lca] + 1)
    answer += depth[lca]
  return answer

print(Part1())
print(Part2())
