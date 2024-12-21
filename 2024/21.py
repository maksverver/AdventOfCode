# Advent of Code 2024 Day 21: Keypad Conundrum
# https://adventofcode.com/2024/day/21

from functools import cache
import sys

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

codes = sys.stdin.read().splitlines()

# Returns a list of all possible paths from character `src` to `dst` on the
# given keypad, with sequences with unnecessary alternations removed (e.g. the
# result could contain "^^>" and ">^^" but not "^>^"), which means the result
# has either 1 or 2 elements.
@cache
def Paths(keypad_id, src, dst):
    keypad = keypads[keypad_id]
    for r, row in enumerate(keypad):
         for c, ch in enumerate(row):
            if ch == src: r1, c1 = r, c
            if ch == dst: r2, c2 = r, c
    dr = r2 - r1
    dc = c2 - c1
    if dr == 0: return ['<>'[dc > 0] * abs(dc)]  # horizontal only
    if dc == 0: return ['^v'[dr > 0] * abs(dr)]  # vertical only
    options = []
    if keypad[r2][c1] != ' ': options.append('^v'[dr > 0] * abs(dr) + '<>'[dc > 0] * abs(dc))  # vertical first
    if keypad[r1][c2] != ' ': options.append('<>'[dc > 0] * abs(dc) + '^v'[dr > 0] * abs(dr))  # horizontal first
    return options


def Solve(num_robots):

    # Determines the number of human keypresses required to type string s on the
    # given level, assuming the robots this and all level above it are in the
    # 'A' position.
    #
    # Level 0 is the level with the numerical keypad, higher levels have remote
    # controls with cursor keys. The human at level (num_robots + 1) can
    # press buttons directly, while robots must controlled by higher level
    # robots.
    #
    # Note that since typing a character requires a higher-level robot (or
    # human) to press 'A', that means that whenever a letter is typed on this
    # level, the robots on all higher levels must have returned to the 'A'
    # position.
    @cache
    def Length(s, level):
        if level > num_robots:
            # Human operator can just type the string with his fingers.
            return len(s)
        
        # Type each character in sequence; when multiple options exist to move
        # between characters, pick the one that minimizes the work done by the
        # upper levels.
        keypad_id = int(level > 0)
        total = 0
        last_ch = 'A'
        for ch in s:
            total += min(Length(t + 'A', level + 1) for t in Paths(keypad_id, last_ch, ch))
            last_ch = ch
        return total

    return sum(Length(code, 0) * int(code.rstrip('A')) for code in codes)

print(Solve(2))   # part 1
print(Solve(25))  # part 2
