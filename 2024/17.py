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

# Part 1: calculate the output with the given initial register values.
answer1 = ','.join(map(str, Run()))
print(answer1)

assert answer1 == ','.join(map(str, Run2()))
assert answer1 == ','.join(map(str, Run3()))

# Part 2: find the initial register value that causes the program to print
# its own source code.
#
# Since we know each iteration of the loop consumes 3 bits from A, and we
# end with A=0, we can reconstruct possible A's backward, by trying all
# values of the 3 bits added during a loop, essentially running the program
# backwards. This is much faster than the forward approach, since we only
# have 8 options at every step, plus we do not have to consider the case
# where we invalidate earlier solutions.
def SolveBackward(A, i):
    if i == 0: return A
    return min((SolveBackward((A << 3) + x, i - 1) for x in range(8)
            if DecodeOne((A << 3) + x) == program[i - 1]), default=inf)

answer2 = SolveBackward(0, len(program))
print(answer2)

# Calculates the length of the prefix of the program that is correctly
# reproduced by starting with register value A:
def ValidPrefixLength(A):
    i = 0
    while A != 0 and i < len(program) and DecodeOne(A) == program[i]:
        i += 1
        A >>= 3
    return i

# Alternate solution, which reconstructs the answer from front to back
# instead. This was the approach I originally used to solve the problem,
# but it is much slower.
#
# The idea is that the i-th output value depends only on bits 3i through
# 3i + 10 (exclusive) in the input, so we can move through the output values
# from left to right, and try each possible 10-bit pattern to add to A,
# while checking we are not invalidating any earlier answers.
@cache
def SolveForward(i, A):
    shift = 3*i

    if i == len(program):
        return inf if (A >> shift) != 0 else A

    return min((SolveForward(i + 1, A + (j << shift)) for j in range(2**10)
            if ValidPrefixLength(A + (j << shift)) > i), default=inf)

#assert answer2 == SolveForward(0, 0)
