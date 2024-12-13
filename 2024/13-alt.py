# Alternate solution using a closed form expression.

import re
import sys

# Let's call `na` and `nb` the number of times we press button A and B,
# respectively. Then we have:
#
#  x = xa * na + xb * nb
#  y = ya * nb + yb * nb
#
# Note that we have only two variables (na, nb), the others are constants.
#
# Equivalently:
#
#  x - xa * na = xb * nb
#  y - ya * nb = yb * nb
#
# And looking at the ratio:
#
#  (x - xa*na) / (y - ya*na) = xb*nb / yb*nb = xb / yb
#
# Now we have eliminated nb, we can solve for na:
#
#  (x - xa*na) * yb = xb * (y - ya*na)
#
#  x*yb - xa*yb*na = y*xb - xb*ya*na
#
#  (xb*ya - xayb)*na = y*xb - x*yb
#
#  na = (y*xb - x*yb) / (xb*ya - xa*yb)
#
# We can calculate `nb` symmetrically, and of course, both values must be
# nonnegative integers for the solution to be valid.
#
# Note that this assumes the solution (if it exists) is uniquely determined,
# which is the case when xa/ya and xb/yb differ from x/y, which happens to be
# the case for all samples in the input.
#
def SolveCase(xa, ya, xb, yb, x, y):
    assert xa*y != ya*x  # xa / ya != x / y
    assert xb*y != yb*x  # xb / yb != x / y

    nom_a = y*xb - x*yb
    den_a = xb*ya - xa*yb
    if nom_a % den_a != 0:
        return None
    na = nom_a // den_a
    if na < 0:
        return None

    nom_b = y*xa - x*ya
    den_b = xa*yb - xb*ya
    if nom_b % den_b != 0:
        return None
    nb = nom_b // den_b
    if nb < 0:
        return None

    return 3*na + 1*nb


cases = [tuple(int(s) for s in re.findall(r'\d+', paragraph))
         for paragraph in sys.stdin.read().split('\n\n')]

def Solve(extra):
    answer = 0
    for ax, ay, bx, by, x, y in cases:
        cost = SolveCase(ax, ay, bx, by, x + extra, y + extra)
        if cost is not None:
            answer += cost
    return answer

# Part 1
print(Solve(0))

# Part 2
print(Solve(10000000000000))
