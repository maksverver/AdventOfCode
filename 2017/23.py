from collections import deque
import sys

REG_IP = '_ip_'
REG_SENDCOUNT = '_mulcount_'

def Load(regs, operand):
    if operand.isidentifier():
        return regs.get(operand, 0)
    else:
        return int(operand)

def Step(instructions, regs):
    opcode, *args = instructions[regs[REG_IP]]
    regs[REG_IP] += 1
    if opcode == 'set':
        regs[args[0]] = Load(regs, args[1])
    elif opcode == 'sub':
        regs[args[0]] = Load(regs, args[0]) - Load(regs, args[1])
    elif opcode == 'mul':
        regs[args[0]] = Load(regs, args[0]) * Load(regs, args[1])
        if REG_SENDCOUNT in regs:
            regs[REG_SENDCOUNT] += 1
    elif opcode == 'jnz':
        if Load(regs, args[0]):
            regs[REG_IP] += Load(regs, args[1]) - 1
    else:
        assert False

def Part1(instructions):
    regs = {REG_IP: 0, REG_SENDCOUNT: 0}
    while 0 <= regs[REG_IP] < len(instructions):
        Step(instructions, regs)
    return regs[REG_SENDCOUNT]

def IsPrime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x%2 == 0:
        return False
    for d in range(3, int(x**.5) + 1, 2):
        if x%d == 0:
            return False
    return True

def Part2():
    # manually optimized program
    return sum(not IsPrime(x) for x in range(108100, 125101, 17))

instructions = [tuple(line.split()) for line in sys.stdin]
print(Part1(instructions))
print(Part2())
