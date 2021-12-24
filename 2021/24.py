import re
import sys

def Add(x, y):
    return x + y

def Mul(x, y):
    return x * y

def Div(x, y):
    assert x >= 0 and y > 0
    return x // y

def Mod(x, y):
    assert x >= 0 and y > 0
    return x % y

def Eql(x, y):
    return int(x == y)

operators = {
    'add': Add,
    'mul': Mul,
    'div': Div,
    'mod': Mod,
    'eql': Eql,
}

class Machine:
    def __init__(self, input):
        self.regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        self.input_data = input
        self.input_pos = 0

def GenInput(dst):
    assert dst in 'wxyz'
    def Inp(m):
        m.regs[dst] = m.input_data[m.input_pos]
        m.input_pos += 1
    return Inp

def GenOpRegister(op, dst, src):
    assert src in 'wxyz'
    assert dst in 'wxyz'
    def Op(m):
        m.regs[dst] = op(m.regs[dst], m.regs[src])
    return Op

def GenOpImmediate(op, dst, val):
    assert dst in 'wxyz'
    def Op(m):
        m.regs[dst] = op(m.regs[dst], val)
    return Op

def ParseInstruction(line):
    opcode, *operands = line.split()
    if opcode == 'inp':
        dst, = operands
        return GenInput(dst)
    op = operators[opcode]
    dst, src = operands
    if src in 'wxyz':
        return GenOpRegister(op, dst, src)
    return GenOpImmediate(op, dst, int(src))

def EvalZInterpreted(code):
    m = Machine(code)
    for i, f in enumerate(instructions):
        f(m)
    return m.regs['z']

instructions = [ParseInstruction(line) for line in sys.stdin]


# Analysis: the instruction list contains 14 copies of the following code:
#
#    0 inp w
#    1 mul x 0
#    2 add x z
#    3 mod x 26
#    4 div z <<DIVZ>>
#    5 add x <<ADDX>>
#    6 eql x w
#    7 eql x 0
#    8 mul y 0
#    9 add y 25
#   10 mul y x
#   11 add y 1
#   12 mul z y
#   13 mul y 0
#   14 add y w
#   15 add y <<ADDY>>
#   16 mul y x
#   17 add z y
#
# Where only the operands on lne 4, 5 and 15 differ.

#          0    1    2    3    4    5    6    7    8    9   10   11   12   13
divz = [   1,   1,   1,  26,  26,   1,  26,  26,   1,   1,  26,   1,  26,  26]
addx = [  12,  13,  13,  -2, -10,  13, -14,  -5,  15,  15, -14,  10, -14,  -5]
addy = [   7,   8,  10,   4,   4,   6,  11,  13,   1,   8,   4,  13,   4,  14]

def EvalZ(code):
    z = 0
    for i, w in enumerate(code):
        x = z % 26 + addx[i]
        z //= divz[i]
        if x != w:
            z = 26*z + w + addy[i]
    return z

# limz[i] - 1 is the maximum value so that a solution is still possible at index i
limz = [0]*15
limz[14] = 1
for i in reversed(range(14)):
    limz[i] = divz[i] * limz[i + 1]


def Solve(digits):
    def Search(i, z):
        if z >= limz[i]:
            return None  # no solution possible

        if i == 14:
            assert z == 0
            return tuple()  # solution found!

        for digit in digits:
            zz = z // divz[i]
            if z % 26 + addx[i] != digit:
                zz = 26*zz + digit + addy[i]
            result = Search(i + 1, zz)
            if result is not None:
                return (digit,) + result

    return Search(0, 0)


digits1 = [9, 8, 7, 6, 5, 4, 3, 2, 1]
digits2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for digits in [digits1, digits2]:
    code = Solve(digits)
    print(''.join(map(str, code)))

    # Sanity checking:
    assert EvalZ(code) == 0
    assert EvalZInterpreted(code) == 0
