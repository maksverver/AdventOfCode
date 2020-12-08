import sys

def ParseInstruction(line):
    opcode, operand = line.split()
    return (opcode, int(operand))

def Evaluate(program):
    ip = 0
    acc = 0
    executed = set()
    while ip not in executed and 0 <= ip < len(program):
        executed.add(ip)
        opcode, operand = program[ip]
        if opcode == 'nop':
            ip += 1
        elif opcode == 'jmp':
            ip += operand
        elif opcode == 'acc':
            acc += operand
            ip += 1
        else:
            assert False, acc
    return ip, acc

program = list(map(ParseInstruction, sys.stdin))

# Part 1: print accumulator value where program loops
ip, acc = Evaluate(program)
assert 0 <= ip < len(program)
print(acc)

# Part 2: modify program so it doesn't loop
for i, (opcode, operand) in enumerate(program):
    if opcode == 'nop':
        program[i] = ('jmp', operand)
    elif opcode == 'jmp':
        program[i] = ('nop', operand)
    else:
        continue
    ip, acc = Evaluate(program)
    if ip < 0 or ip >= len(program):
        assert ip == len(program)
        print(acc)
    program[i] = (opcode, operand)
