from functools import reduce
import re
import sys

pattern = re.compile('fold along ([xy])=(\d+)')

def ParsePoint(line):
    x, y = map(int, line.split(','))
    return (x, y)

def FoldX(fold_x):
    def transform(point):
        x, y = point
        return (x if x < fold_x else 2*fold_x - x, y)
    return transform
            
def FoldY(fold_y):
    def transform(point):
        x, y = point
        return (x, y if y < fold_y else 2*fold_y - y)
    return transform

def ParseTransform(line):
    axis, value = pattern.match(line).groups()
    if axis == 'x':
        return FoldX(int(value))
    elif axis == 'y':
        return FoldY(int(value))

def ApplyTransforms(point, transforms):
    for transform in transforms:
        point = transform(point)
    return point
    
points, transforms = sys.stdin.read().rstrip().split('\n\n')
points = [ParsePoint(line) for line in points.split('\n')]
transforms = [ParseTransform(line) for line in transforms.split('\n')]

# Part 1
visible = set(transforms[0](p) for p in points)
print(len(visible))

# Part 2
visible = set(ApplyTransforms(p, transforms) for p in points)
min_x = min(x for (x, y) in visible)
min_y = min(y for (x, y) in visible)
max_x = max(x for (x, y) in visible)
max_y = max(y for (x, y) in visible)
for y in range(min_y, max_y + 1):
    print(''.join('.#'[(x, y) in visible] for x in range(min_x, max_x + 1)))

