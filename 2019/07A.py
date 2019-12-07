from itertools import permutations
from operator import add, mul, lt, eq
import sys

initial_ints = list(map(int, sys.stdin.readline().split(',')))

def RunMachine(inputs):
    outputs = []

    def get():
        nonlocal inputs
        input, inputs = inputs[0], inputs[1:]
        return input

    def put(output):
        outputs.append(output)

    def jit(cond, new_ip, cur_ip):
        return new_ip if cond != 0 else cur_ip

    def jif(cond, new_ip, cur_ip):
        return new_ip if cond == 0 else cur_ip

    opcode_map = {
      1: ('IIO', add),
      2: ('IIO', mul),
      3: ('O', get),
      4: ('I', put),
      5: ('IIP', jit),
      6: ('IIP', jif),
      7: ('IIO', lt),
      8: ('IIO', eq),
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
        update_ip = False
        for i, t in enumerate(params):
            if t == 'P':
                args.append(ip)
                update_ip = True
                break
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
        if update_ip:
            assert not dests
            ip = result
        for i in dests:
            ints[i] = result

    return outputs

def CalculateOutputSignal(phases):
    signal = 0
    for phase in phases:
        signal, = RunMachine([phase, signal])
    return signal

print(max(CalculateOutputSignal(phases) for phases in permutations(range(5))))
