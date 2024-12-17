# More generic solution for Day 17. It works for any input file that has roughly
# the same structure as mine (see 17.py for details), so it should work for all
# official Advent of Code inputs given to different contestants.

from math import inf
import re
import sys

initial_A, program = re.match('''^\
Register A: (\\d+)
Register B: 0
Register C: 0

Program: ([0-7](?:,[0-7])+)\
$'''.strip(), sys.stdin.read().strip()).groups()

initial_A = int(initial_A)
program = tuple(map(int, program.split(',')))

# Check some constraints on the input program
opcodes  = program[0::2]
operands = program[1::2]
instructions = tuple(zip(opcodes, operands))
assert instructions[-1] == (3, 0)   # Last instruction is "jnz 0"
assert 3 not in opcodes[:-1]        # No other jumps occur
assert opcodes.count(5) == 1        # Exactly one "out" instruction in the loop
assert opcodes.count(0) == 1        # Exactly one "adv" instruction in the loop
assert (0, 3) in instructions       # .. and it's "adv 3"
# Should check B and C are not preserved across loops

def Run(A=initial_A, B=0, C=0):
    ip = 0
    while 0 <= ip < len(program):
        opcode, operand = program[ip:(ip:=ip+2)]
        combo = [0, 1, 2, 3, A, B, C, None][operand]
        if   opcode == 0: A >>= combo
        elif opcode == 1: B ^= operand
        elif opcode == 2: B = combo & 7
        elif opcode == 3: ip = operand if A else ip
        elif opcode == 4: B = B ^ C
        elif opcode == 5: yield (combo & 7)
        elif opcode == 6: B = A >> combo
        elif opcode == 7: C = A >> combo
        else:             assert False

def DecodeOne(A):
    for out in Run(A):
        return out

# Part 1
print(*Run(), sep =',')

def SolveBackward(A, i):
    if i == 0: return A
    return min((SolveBackward((A << 3) + x, i - 1) for x in range(8)
            if DecodeOne((A << 3) + x) == program[i - 1]), default=inf)

# Part 2
print(SolveBackward(0, len(program)))
