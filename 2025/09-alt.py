# Advent of Code 2025 day 9 (https://adventofcode.com/2025/day/9)
#
# This solution considers the outline of the figure and rectangles.
#

from itertools import combinations
import sys

def Clamp(min, x, max):
    if x < min: return min
    if x > max: return max
    return x

def Subcycles(a, n):
    '''Generates all cyclic sybarrays of a of length n.

    For example, Subcycles([1, 2, 3, 4, 5], 3) yields
        (1, 2, 3)
        (2, 3, 4)
        (3, 4, 5)
        (4, 5, 1)
        (5, 1, 2)
    '''
    return zip(*(a[i:] + a[:i] for i in range(n)))

def Area(poly):
    '''Calculates twice the signed area of a polygon using the Shoelace formula'''
    return sum(x1*y2 - y1*x2 for ((x1, y1), (x2, y2)) in Subcycles(poly, 2))

# Read points in input
points = [tuple(map(int, line.split(','))) for line in sys.stdin]

# First, we calculate all potential rectangles and their areas.
#
# The result is a list of (area, x1, y1, x2, y2) tuples.
rectangles = []
for (x1, y1), (x2, y2) in combinations(points, 2):
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    rectangles.append(((x2 - x1 + 1)*(y2 - y1 + 1), x1, y1, x2 + 1, y2 + 1))

# Sort the rectangles because we will check them in order of decreasing area below.
rectangles.sort(reverse=True)

# Part 1: print the largest rectangle's area
print(rectangles[0][0])

# This condition checks that the points in the polygon are given in clockwise
# order. If not, we'd have to reverse the points.
assert Area(points) > 0

# First we need to convert the figure to its outline. This is mildly tricky
# because edges have unit width, so depending on how the corners turn we must
# add 0 or 1 to the x and y coordinates. The logic below depends on the points
# being ordered in clockwise direction.
polygon = []
for (x0, y0), (x1, y1), (x2, y2) in Subcycles(points, 3):
    assert (x0 == x1) != (y0 == y1) != (y1 == y2) != (x1 == x2)
    if (y0 > y1 and x2 > x1) or (x0 < x1 and y2 < y1): polygon.append((x1 + 0, y1 + 0))
    if (x0 < x1 and y2 > y1) or (y0 < y1 and x2 > x1): polygon.append((x1 + 1, y1 + 0))
    if (x0 > x1 and y2 < y1) or (y0 > y1 and x2 < x1): polygon.append((x1 + 0, y1 + 1))
    if (y0 < y1 and x2 < x1) or (x0 > x1 and y2 > y1): polygon.append((x1 + 1, y1 + 1))

# Now for part 2, we need to find the largest rectangle that completely overlaps
# the figure. To check, we can calculate the area of the polygon after clamping
# its coordinates to the rectangle.
for area, x1, y1, x2, y2 in sorted(rectangles, key=lambda t: t[0], reverse=True):
    if Area([(Clamp(x1, x, x2), Clamp(y1, y, y2)) for (x, y) in polygon]) == area*2:
        print(area)
        break
