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
        assert 0 <= reg < 4
        return regs[reg]

    def Store(reg, val):
        assert 0 <= reg < 4
        regs[reg] = val

    def Arg(p, o):
        if p == 'i': return o
        if p == 'r': return Load(o)
        if p == '0': return 0

    assert len(operands) == 3
    params, operation = instruction_set[mnem]
    Store(operands[2], operation(Arg(params[0], operands[0]), Arg(params[1], operands[1])))

def ExecuteStep(regs, mnem, args):
    regs = list(regs)
    Execute(regs, mnem, args)
    return tuple(regs)

def ParseSample(string):
    numbers = tuple(map(int, re.findall(r'-?\d+', string)))
    assert len(numbers) == 12
    return (numbers[0:4], numbers[4:8], numbers[8:12])

def Part1(samples):
    def CountPossibilities(sample):
        before, instr, after = sample
        args = instr[1:4]
        return sum(ExecuteStep(before, mnem, args) == after for mnem in mnemonics)

    return sum(CountPossibilities(sample) >= 3 for sample in samples)

def Part2(samples, program):
    # For each opcode, calculate the set of possible mnemonics.
    possible_mnemnonics = [set(mnemonics) for _ in range(16)]
    for before, instr, after in samples:
        opcode = instr[0]
        args = instr[1:4]
        possible_mnemnonics[opcode].intersection_update(
            mnem for mnem in mnemonics if ExecuteStep(before, mnem, args) == after)

    # Calculate opcode map, by fixing each opcode that has only a single possible
    # mnemonic, then removing that mnemonic from the other possiblities.
    opcode_map = [None]*16
    while not all(opcode_map):
        for i, a in enumerate(possible_mnemnonics):
            if opcode_map[i] is None and len(a) == 1:
                mnem, = a
                for b in possible_mnemnonics:
                    b.discard(mnem)
                opcode_map[i] = mnem

    # Evaluate sample program.
    regs = [0, 0, 0, 0]
    for o, *args in program:
        Execute(regs, opcode_map[o], args)
    return regs[0]

data = sys.stdin.read()
first, second = data.split('\n\n\n')
samples = [ParseSample(string) for string in first.split('\n\n')]
program = [tuple(map(int, line.split())) for line in second.strip().split('\n')]
print(Part1(samples))
print(Part2(samples, program))
