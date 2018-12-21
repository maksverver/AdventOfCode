import re
import sys

add = lambda a, b: a + b
mul = lambda a, b: a * b
ban = lambda a, b: a & b
bor = lambda a, b: a | b
gt = lambda a, b: int(a > b)
eq = lambda a, b: int(a == b)
instruction_set = {
    'addr': ('rr', add),
    'addi': ('ri', add),
    'mulr': ('rr', mul),
    'muli': ('ri', mul),
    'banr': ('rr', ban),
    'bani': ('ri', ban),
    'borr': ('rr', bor),
    'bori': ('ri', bor),
    'setr': ('r0', add),
    'seti': ('i0', add),
    'gtir': ('ir', gt),
    'gtri': ('ri', gt),
    'gtrr': ('rr', gt),
    'eqir': ('ir', eq),
    'eqri': ('ri', eq),
    'eqrr': ('rr', eq),
}
mnemonics = tuple(instruction_set)

def Execute(regs, mnem, operands):
    def Load(reg):
        assert 0 <= reg < 6
        return regs[reg]

    def Store(reg, val):
        assert 0 <= reg < 6
        regs[reg] = val

    def Arg(p, o):
        if p == 'i': return o
        if p == 'r': return Load(o)
        if p == '0': return 0

    assert len(operands) == 3
    params, operation = instruction_set[mnem]
    Store(operands[2], operation(Arg(params[0], operands[0]), Arg(params[1], operands[1])))

line = sys.stdin.readline().strip()
a, b = line.split()
assert a == '#ip'
reg_ip = int(b)
instructions = []
for line in sys.stdin:
    mnem, a, b, c = line.split()
    assert mnem in mnemonics
    args = tuple(map(int, (a, b, c)))
    instructions.append((mnem, args))

def Run(reg0):
    regs = [reg0] + 5*[0]
    ip = 0
    while 0 <= ip < len(instructions):
        regs[reg_ip] = ip
        mnem, args = instructions[ip]
        Execute(regs, mnem, args)
        ip = regs[reg_ip] + 1
    return regs[0]

print(Run(0))
