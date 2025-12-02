import sys

answer = 50
for line in sys.stdin:
    if line[0] == 'L':
        x = answer % 100
        if x != 0: answer = answer - x + (100 - x)

    answer += int(line[1:])

    if line[0] == 'L':
        x = answer % 100
        if x != 0: answer = answer - x + (100 - x)

print(answer // 100)
