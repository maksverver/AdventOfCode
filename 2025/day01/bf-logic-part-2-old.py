import sys

answer = 0
val = 50
for line in sys.stdin:
    n = int(line[1:])
    x = n % 100
    answer += n // 100

    if line[0] == 'L':
        if val != 0:
            val = 100 - val

    for _ in range(x):
        if val == 0:
            val = 99
        else:
            val -= 1
            if val == 0:
                answer += 1

    if line[0] == 'L':
        if val != 0:
            val = 100 - val

    #print(line.strip(), val, answer)
    assert 0 <= val < 100

print(answer)
