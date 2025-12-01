import sys

answer = 0

def ParseLine(line):
    ch, n = line[0], line[1:]
    n = int(n)
    assert n > 0
    if ch == 'L': return -n
    if ch == 'R': return +n
    assert False

moves = list(map(ParseLine, sys.stdin))

def Part1():
    answer = 0
    i = 50
    for n in moves:
        i = (i + n) % 100
        answer += i == 0
    return answer

def Part2():
    answer = 0
    i = 50
    for n in moves:
        if n > 0 and i + n >= 100:
            answer += (i + n) // 100
        if n < 0:
            answer += -(i + n) // 100 + (i > 0)
        i = (i + n) % 100
    return answer

print(Part1())
print(Part2())
