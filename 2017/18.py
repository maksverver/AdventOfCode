from collections import deque
import sys

REG_IP = '_ip_'
REG_BLOCKED = '_blocked_'
REG_SENDCOUNT = '_sendcount_'

def Load(regs, operand):
    if operand.isidentifier():
        return regs.get(operand, 0)
    else:
        return int(operand)

def Step(instructions, regs, input, output):
    opcode, *args = instructions[regs[REG_IP]]
    regs[REG_IP] += 1
    if opcode == 'snd':
        if REG_SENDCOUNT in regs:
            regs[REG_SENDCOUNT] += 1
        output.append(Load(regs, args[0]))
    elif opcode == 'rcv':
        if len(input) > 0:
            regs[args[0]] = input.popleft()
            regs[REG_BLOCKED] = 0
        else:
            regs[REG_BLOCKED] = 1
            regs[REG_IP] -= 1
    elif opcode == 'set':
        regs[args[0]] = Load(regs, args[1])
    elif opcode == 'add':
        regs[args[0]] = Load(regs, args[0]) + Load(regs, args[1])
    elif opcode == 'mul':
        regs[args[0]] = Load(regs, args[0]) * Load(regs, args[1])
    elif opcode == 'mod':
        regs[args[0]] = Load(regs, args[0]) % Load(regs, args[1])
    elif opcode == 'jgz':
        if Load(regs, args[0]) > 0:
            regs[REG_IP] += Load(regs, args[1]) - 1
    else:
        assert False

def Part1(instructions):
    regs = {REG_IP: 0, REG_BLOCKED: 0}
    output = []
    while not regs[REG_BLOCKED]:
        Step(instructions, regs, [], output)
    return output[-1]

def Part2(instructions):
    regs0 = {REG_IP: 0, REG_BLOCKED: 0, 'p': 0}
    regs1 = {REG_IP: 0, REG_BLOCKED: 0, 'p': 1, REG_SENDCOUNT: 0}
    queue0 = deque()
    queue1 = deque()
    while not (regs0[REG_BLOCKED] and regs1[REG_BLOCKED]):
        Step(instructions, regs0, queue0, queue1)
        Step(instructions, regs1, queue1, queue0)
    return regs1[REG_SENDCOUNT]

instructions = [tuple(line.split()) for line in sys.stdin]
print(Part1(instructions))
print(Part2(instructions))
