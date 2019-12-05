import sys

ints = list(map(int, sys.stdin.readline().split(',')))

ints[1] = 12
ints[2] = 2

ip = 0
while ints[ip] != 99:
    a, b, c, d = ints[ip:ip + 4]
    if a == 1:
        ints[d] = ints[b] + ints[c]
    elif a == 2:
        ints[d] = ints[b] * ints[c]
    else:
        assert False
    ip += 4


print(ints[0])
