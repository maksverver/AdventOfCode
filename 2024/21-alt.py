# Advent of Code 2024 Day 21: Keypad Conundrum
# https://adventofcode.com/2024/day/21
#
# Alternate solution which uses only a single static expansion of each path,
# instead of up to 2 different expansions returned by Paths() in 21-alt.py.

from functools import cache, reduce
import sys

sample_codes = ['029A', '980A', '179A', '456A', '379A']

keypads = [
    [
        '789',
        '456',
        '123',
        ' 0A',
    ],
    [
        ' ^A',
        '<v>',
    ],
]

# Returns an optimal path from character `src` to `dst` on the given keypad.
#
# It turns out there is a heuristic that can be used to generate an optimal
# path, choosing between any two alternatives. For example, "v>" is better than
# ">v" because:
# 
#   "v>A" => "<vA>A^A" => "v<<A>A^>AvA^A<A>A"
#   ">vA" => "vA<A^>A" => "<vA^>Av<<A>>^A<Av>A^A"
#
# The intuition here is that we can split each string on A's and treat them
# independently:
#
#   "v>A => {"<vA", ">A", "^A"}
#   ">vA => {"vA", "^>A", "<A"}
#
# And:
#
#  "<vA"     => {"v<<A", ">A", "^>A"} 4 + 2 + 3 =  9
#  ">A"      => {"vA", "^A"}          2 + 2     =  4
#  "^A"      => {"<A", ">A"}          2 + 2     =  4 +
#                                                -----
#                                                 17
#
#  "vA"      => {}"<vA", "^>A"}       3 + 3     =  6
#  "<A"      => {}"v<<A", ">>^A"}     4 + 4     =  8
#  "^>A"     => {}"<A", "v>A", "^A"}  2 + 3 + 2 =  7
#                                                -----
#                                                 21
#
# So for each of the four directions ^/>, ^/<, v/<, v/> there is an optimal
# order of either moving horizontally or vertically first. At first I thought
# this order might be specific to the level where we operate, but it turns out
# that there is a single optimal order that works on all levels, which I found
# emperically and are encoded in the bottom four lines of the function below:
def GetPath(keypad_id, src, dst):
    keypad = keypads[keypad_id]
    for r, row in enumerate(keypad):
         for c, ch in enumerate(row):
            if ch == src: r1, c1 = r, c
            if ch == dst: r2, c2 = r, c
    dr = r2 - r1
    dc = c2 - c1
    horiz = '<>'[dc > 0] * abs(dc)
    verti = '^v'[dr > 0] * abs(dr)
    if dr == 0: return horiz
    if dc == 0: return verti
    if keypad[r2][c1] == ' ': return horiz + verti  # can't go vertical first
    if keypad[r1][c2] == ' ': return verti + horiz  # can't go horizontal first
    # This is the secret sauce. These results have been determined empirically.
    if dr < 0 and dc < 0: return horiz + verti  # prefer "<v" over "v<"
    if dr < 0 and dc > 0: return verti + horiz  # prefer "v>" over ">v"
    if dr > 0 and dc < 0: return horiz + verti  # prefer "<v" over "v<"
    if dr > 0 and dc > 0: return verti + horiz  # prefer "v>" over ">v"


# Several solutions follow, all using GetPath() declared above. One is that
# we can start with the input sequence on level 0 (where the real door keypad is)
# and then expand this string by replacing each character with the path to
# generate it at the higher level:

def ExpandIterative(code, robots):
    s = code
    for level in range(robots + 1):
        last = 'A'
        t = ''
        for ch in s:
            t += GetPath(level > 0, last, ch) + 'A'
            last = ch
        s = t
    return t

def SolveIterative(code, robots):
    return len(ExpandIterative(code, robots))


# We can rewrite this as a recursive function, the benefit of which will become
# clear later; for now, notice the similarity in the implementation, and that
# instead of iteration on `s`, we simply pass `s` down the recursive calls:

def ExpandRecursive(s, level, robots):
    if level > robots:
        return s
    last = 'A'
    t = ''
    for ch in s:
        t += ExpandRecursive(GetPath(level > 0, last, ch) + 'A', level + 1, robots)
        last = ch
    return t

def SolveRecursive(code, robots):
    return len(ExpandRecursive(code, 0, robots))

# The recursive solution can be modified to only compute the length, and not
# the actual string generated. This is necessary for part 2, since the final
# string is very large, but we only need to know its length.
#
# Note how Calc() mirrors the implementation of ExpandRecursive() though
# instead of returning strings we return string lengths. This allows efficient
# caching of intermediate results:

def SolveMemoized(code, robots):
    @cache
    def Calc(s, level):
        if level > robots:
            return len(s)
        last = 'A'
        res = 0
        for ch in s:
            res += Calc(GetPath(level > 0, last, ch) + 'A', level + 1)
            last = ch
        return res

    return Calc(code, 0)


# Now that we know how to find the length of the final input sequence for
# a single code, we can define a solve function that solves each code in the
# input and calculates the combined answer:

def Solve(solve, codes, robots):
    return sum(solve(code, robots) * int(code.rstrip('A')) for code in codes)


# Verify samples
assert Solve(SolveIterative, sample_codes,  2) == 126384
assert Solve(SolveRecursive, sample_codes,  2) == 126384
assert Solve(SolveMemoized,  sample_codes,  2) == 126384
assert Solve(SolveMemoized,  sample_codes, 25) == 154115708116294

# Solve real test case
codes = sys.stdin.read().splitlines()
for robots in (2, 25):
    print(Solve(SolveMemoized, codes, robots))
