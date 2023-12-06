import sys

# Read input
time_head, *times = sys.stdin.readline().split()
dist_head, *dists = sys.stdin.readline().split()
assert time_head == 'Time:'
assert dist_head == 'Distance:'
times = list(map(int, times))
dists = list(map(int, dists))
assert len(times) == len(dists)

def CountWinning(t, d):
  def IsWinning(hold):
    return (t - hold)*hold > d

  x = t // 2
  if not IsWinning(x): return 0

  def LowerBound():
    lo, hi = 0, x
    while lo < hi:
      mid = (lo + hi) // 2
      if IsWinning(mid):
        hi = mid
      else:
        lo = mid + 1
    return lo

  def UpperBound():
    lo, hi = x, t
    while lo < hi:
      mid = (lo + hi) // 2
      if not IsWinning(mid):
        hi = mid
      else:
        lo = mid + 1
    return lo

  a = LowerBound()
  b = UpperBound()
  assert not IsWinning(a - 1) and IsWinning(a)
  assert IsWinning(b - 1) and not IsWinning(b)
  return b - a


# Part 1
answer1 = 1
for t, d in zip(times, dists):
  answer1 *= CountWinning(t, d)
print(answer1)

# Part 2
t = int(''.join(map(str, times)))
d = int(''.join(map(str, dists)))
print(CountWinning(t, d))
