import sys

program = [int(s) for s in sys.stdin.readline().split(',')]
for ip in range(0, len(program), 2):
    opcode = program[ip]
    operand = program[ip + 1]
    mnemonic = pseudocode = None
    if opcode == 0:
        mnemonic = 'adv'
        pseudocode = 'A >>= COMBO'
    elif opcode == 1:
        mnemonic = 'bxl'
        pseudocode = 'B ^= LITERAL'
    elif opcode == 2:
        mnemonic = 'bst'
        pseudocode = 'B = COMBO & 7'
    elif opcode == 3:
        mnemonic = 'jnz'
        pseudocode = 'if A != 0: goto LITERAL'
    elif opcode == 4:
        mnemonic = 'bxc'
        pseudocode = 'B ^= C'
    elif opcode == 5:
        mnemonic = 'out'
        pseudocode = 'yield (COMBO & 7)'
    elif opcode == 6:
        mnemonic = 'bdv'
        pseudocode = 'B = A >> COMBO'
    elif opcode == 7:
        mnemonic = 'cdv'
        pseudocode = 'C = A >> COMBO'
    else:
        assert False

    if 'COMBO' in pseudocode:
        arg = ['0', '1', '2', '3', 'A', 'B', 'C'][operand]
        pseudocode = pseudocode.replace('COMBO', arg)
    elif 'LITERAL' in pseudocode:
        arg = str(operand)
        pseudocode = pseudocode.replace('LITERAL', arg)
    else:
        arg = '-'
    print('%3d: %d %d    %s %s    %s' % (ip, opcode, operand, mnemonic, arg, pseudocode))
