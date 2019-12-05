import sys

initial_ints = list(map(int, sys.stdin.readline().split(',')))

for i in range(100):
  for j in range(100):
    ints = list(initial_ints)
    ints[1] = i
    ints[2] = j
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
    if ints[0] == 19690720:
        print(100*i + j)
