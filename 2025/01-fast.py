import sys

answer1 = 0
answer2 = 0
i = 50
tot = 0
for line in sys.stdin:
    n = int(line[1:])
    if line[0] == 'L':
        n = -n
    if n > 0:
        answer2 += (i + n) // 100
    if n < 0:
        answer2 += -(i + n) // 100 + (i > 0)
    i = (i + n) % 100
    answer1 += i == 0
    tot += n
print(answer1)
print(answer2)
