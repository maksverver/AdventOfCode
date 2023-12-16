from math import *
import sys

def CountWinning(t, d):

  # Let x be the time the button is helt. Then the time left for travel is
  # (t - x), and the distance traveled is x(t - x). So we have to count the
  # number of (integer) solutions to the inequality:
  #
  #   x(t - x) > d
  #
  # Rewrite:
  #
  #   -x^2 + tx > d
  #   -x^2 + tx - d > 0
  #   x^2 - tx + d < 0
  #
  # Solve with the quadratic formula:
  #
  #  Δ = t^2 - 4d
  #  (t - sqrt(Δ))/2 < x < (t + sqrt(Δ))/2
  #
  # We need to be careful with rounding to convert the bounds!

  delta = t**2 - 4*d
  if delta <= 0: return 0

  # This would work for the official testdata, but uses floating point numbers
  # which have limited precision:
  # min_x = floor((t - sqrt(delta))/2) + 1
  # max_x = ceil((t + sqrt(delta))/2) - 1
  # return max_x - min_x + 1

  # To make this work for arbitrary integer input:
  #
  # Note that ceil(sqrt(x)) can be written exactly as isqrt(x - 1) + 1 (x > 0).
  min_x = (t - isqrt(delta - 1) + 1)//2
  max_x = (t + isqrt(delta - 1)    )//2
  return max_x - min_x + 1


# Read input
time_head, *times = sys.stdin.readline().split()
dist_head, *dists = sys.stdin.readline().split()
assert time_head == 'Time:'
assert dist_head == 'Distance:'
times = list(map(int, times))
dists = list(map(int, dists))
assert len(times) == len(dists)

# Part 1
answer1 = 1
for t, d in zip(times, dists):
  answer1 *= CountWinning(t, d)
print(answer1)

# Part 2
t = int(''.join(map(str, times)))
d = int(''.join(map(str, dists)))
print(CountWinning(t, d))
