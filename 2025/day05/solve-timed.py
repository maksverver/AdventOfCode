import sys
import time

def timed(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            finish = time.perf_counter()
            print(f'{func.__name__}: {(finish - start):.3f} s', file=sys.stderr)
    return wrapper

def ParseRange(line):
    l, r = map(int, line.split('-'))
    return (l, r + 1)

@timed
def ParseInput():
    part1, part2 = sys.stdin.read().strip().split('\n\n')
    return (
        [ParseRange(line) for line in part1.split('\n')],
        [int(line) for line in part2.split('\n')],
    )

@timed
def SortInput():
    ranges.sort()
    ingredients.sort()

@timed
def Part1():
    answer = 0
    i = 0
    for l, r in ranges:
        # Skip rotten ingredients
        while i < len(ingredients) and ingredients[i] < l:
            i += 1
        # Count fresh ingredients
        while i < len(ingredients) and ingredients[i] < r:
            i += 1
            answer += 1
    return answer

@timed
def Part2():
    i = 0
    answer = 0
    for l, r in ranges:
        if i < l:
            i = l
        if i < r:
            answer += r - i
            i = r
    return answer

ranges, ingredients = ParseInput()
SortInput()
print(Part1())
print(Part2())
