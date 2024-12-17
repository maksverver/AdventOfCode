from functools import cache
from math import inf
import sys

# My input for part 2, I assume this is fixed!
program = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]
initial_A = 59590048

# Runs any program by interpreting it.
def Run(A=initial_A, B=0, C=0):
    ip = 0
    while 0 <= ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        combo = [0, 1, 2, 3, A, B, C, None][operand]
        ip += 2
        if opcode == 0:
            A >>= combo
        elif opcode == 1:
            B ^= operand
        elif opcode == 2:
            B = combo & 7
        elif opcode == 3:
            if A: ip = operand
        elif opcode == 4:
            B = B ^ C
        elif opcode == 5:
            yield (combo & 7)
        elif opcode == 6:
            B = A >> combo
        elif opcode == 7:
            C = A >> combo
        else:
            assert False

# Runs my input program, after analyzing its logic by hand:
#
#  0: 2   bst A
#  1: 4  
#  2: 1   bxl 5
#  3: 5  
#  4: 7   cdv B
#  5: 5  
#  6: 0   adv 3
#  7: 3  
#  8: 1   bxl 6
#  9: 6  
# 10: 4   bxc
# 11: 3  
# 12: 5   out B
# 13: 5  
# 14: 3   jnz 0
# 15: 0
#
def Run2(A=initial_A, B=0, C=0):
    while A:
        B = A & 7
        B = B ^ 5
        C = A >> B
        A = A >> 3
        B = B ^ 6
        B = B ^ C
        yield (B & 7)

# Further simplified:

def DecodeOne(A):
    x = (A & 7) ^ 5
    return x ^ 6 ^ (A >> x) & 7

def Run3(A=initial_A, B=0, C=0):
    while A:
        yield DecodeOne(A)
        A >>= 3

# Calculates the length of the prefix of the program that is correctly
# reproduced by starting with register value A:
def ValidPrefixLength(A):
    i = 0
    while A != 0 and i < len(program) and DecodeOne(A) == program[i]:
        i += 1
        A >>= 3
    return i

# Part 1: calculate the output with the given initial register values.
answer1 = ','.join(map(str, Run()))
print(answer1)

assert answer1 == ','.join(map(str, Run2()))
assert answer1 == ','.join(map(str, Run3()))

# Part 2: find the minimum initial register value that causes the program
# to print its own output.
#
# Logic: Run3() removes the lower 3 bits from A after each output, and
# DecodeOne() only uses (at most) the next 10 bits in A, so we can simply
# try reconstructing the program from left to right, trying all possible
# 2**10 = 1024 values, while ensuring that the current prefix remains valid.
#
# (Possible optimization: since changing a bit at position i can only affect
# about 4 output values, we don't need to recheck the entire prefix every
# time, but only from i-3 to i+1. However, the program is short enough that
# this doesn't seem to matter much.)
@cache
def Solve(i, A):
    shift = 3*i

    if i == len(program):
        return inf if (A >> shift) != 0 else A

    return min((Solve(i + 1, A + (j << shift)) for j in range(2**10)
            if ValidPrefixLength(A + (j << shift)) > i), default=inf)

answer2 = Solve(0, 0)
print(answer2)

assert list(Run(answer2)) == program
