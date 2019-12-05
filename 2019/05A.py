from operator import add, mul
import sys

initial_ints = list(map(int, sys.stdin.readline().split(',')))

inputs = [1]
outputs = []

def get():
    global inputs
    input, inputs = inputs[0], inputs[1:]
    return input

def put(a):
    outputs.append(a)

opcode_map = {
  1: ('IIO', add),
  2: ('IIO', mul),
  3: ('O', get),
  4: ('I', put),
}

ints = list(initial_ints)
ip = 0
while ints[ip] != 99:
    rem = ints[ip]
    ip += 1
    opcode = rem % 100
    rem //= 100
    params, func = opcode_map[opcode]
    args = []
    dests = []
    for i, t in enumerate(params):
        assert t in 'IO'
        mode = rem % 10
        rem //= 10
        operand = ints[ip]
        ip += 1
        if t == 'I':
            assert mode in (0, 1)
            if mode == 0:
                arg = ints[operand]
            else:
                arg = operand
            args.append(arg)
        else:
            assert mode == 0
            dests.append(operand)
    result = func(*args)
    for i in dests:
        ints[i] = result

assert all(x == 0 for x in outputs[:-1])
print(outputs[-1])
