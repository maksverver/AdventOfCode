import re
import sys

def Solve(ax, ay, bx, by, x, y):
    a_cost = 3
    b_cost = 1

    # Make ax/ay < bx/by by swapping them if necessary.
    if ax * by > bx * ay:
        ax, ay, bx, by, a_cost, b_cost = bx, by, ax, ay, b_cost, a_cost

    # x/y must lie between ax/ay and bx/by, otherwise it is unsolvable.
    if not (ax/ay <= x/y <= bx/by):
        return None

    # If one or both are exactly equal, we would need to do something different.
    # Fortunately, this doesn't happen with the official testdata.
    assert ax/ay < x/y < bx/by

    # Binary search for `na`, the necessary number of presses of button A,
    # so that the remaining ratio (x - ax*na)/(y - ay*na) = bx / by.
    lo = 0
    hi = y // ay + 1
    while lo < hi:
        na = (lo + hi) // 2
        xleft = x - ax*na
        yleft = y - ay*na
        if xleft * by < bx * yleft:
            # xleft/yleft < bx/by: na is too low.
            lo = na + 1
        elif xleft * by > bx * yleft:
            # xleft/yleft < bx/by: na is too high.
            hi = na
        else:
            # xleft/yleft == bx/by: na is exactly right.
            if xleft % bx != 0:
                # Unsolvable!
                return None
            nb = xleft // bx
            assert xleft == nb * bx and yleft == nb * by
            return na*a_cost + nb*b_cost

    # No value of `na` found: unsolvable!
    return None


answer1 = 0
answer2 = 0
paragraphs = sys.stdin.read().split('\n\n')
for paragraph in paragraphs:
    ax, ay, bx, by, x, y = map(int, re.findall(r'\d+', paragraph))
    assert ax * by != bx * ay
    if (cost := Solve(ax, ay, bx, by, x, y)) is not None:
        answer1 += cost
    x += 10000000000000
    y += 10000000000000
    if (cost := Solve(ax, ay, bx, by, x, y)) is not None:
        answer2 += cost
print(answer1)
print(answer2)
