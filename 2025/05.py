import sys

def ParseRange(line):
    l, r = map(int, line.split('-'))
    return (l, r + 1)

part1, part2 = sys.stdin.read().strip().split('\n\n')
ranges = sorted(ParseRange(line) for line in part1.split('\n'))
ingredients = sorted(int(line) for line in part2.split('\n'))

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

print(Part1())
print(Part2())
