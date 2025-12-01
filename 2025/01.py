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
        i += n
        i %= 100
        answer += i == 0
    return answer

def Part2():
    answer = 0
    i = 50
    for n in moves:
        for _ in range(abs(n)):
            i += n // abs(n)
            i %= 100
            answer += i == 0
    return answer

print(Part1())
print(Part2())
