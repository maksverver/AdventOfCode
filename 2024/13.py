import re
import sys

def SolveCase(ax, ay, bx, by, x, y):
    a_cost = 3
    b_cost = 1

    # Make ax/ay < bx/by by swapping them if necessary.
    if ax * by > bx * ay:
        ax, ay, bx, by, a_cost, b_cost = bx, by, ax, ay, b_cost, a_cost

    # x/y must lie between ax/ay and bx/by, otherwise it is unsolvable.
    if ax * y > x * ay or bx * y < x * by:
        return None

    # If one or both are exactly equal, we would need to do something different.
    # Fortunately, this doesn't happen with the official testdata.
    assert ax * y <= x * ay and bx * y >= x * by

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
