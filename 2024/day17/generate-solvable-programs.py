# Generates all possible programs with the same structure as the official input.
#
# See program.gv for a visualisation of how instructions can be reordered.
#
#  - The operands of the bxl and bxc instructions can vary, for a total of
#    8**3 = 512 different parameter sets.
#
#  - Instructions can be reordered (see program.gv for a visualisation)
#    "bxl y" and "bxc" can be swapped, and "adv 3" can be inserted in 4
#    places (anywhere between "cdv B" and "jnz 0"), for a total of 8
#    different programs up to differences in parameters.
#
# Total number of programs:                4096
# Number of solvable programs:              217
# Minimum solution:              37221261688308
# Maximum solution:             280206214609937

from math import inf
import sys


def GenerateAllPrograms():
    instructions = [
        (2,  4),  # 0: bst A
        (1, -1),  # 1: bxl x
        (7,  5),  # 2: cdv B
        (0,  3),  # 3: adv 3
        (1, -2),  # 4: bxl y
        (4, -3),  # 5: bxc
        (5,  5),  # 6: out B
        (3,  0),  # 7: jnz 0
    ]

    dependencies = [
        (0, 1),
        (0, 3),
        (1, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (4, 6),
        (5, 6),
        (6, 7),
        (3, 7),
    ]

    blocking = [set() for _ in instructions]
    blockers = [set() for _ in instructions]
    for i, j in dependencies:
        blocking[i].add(j)
        blockers[j].add(i)

    def GeneratePrograms(template):
        i = template.index(-1)
        j = template.index(-2)
        k = template.index(-3)
        program = list(template)
        for x in range(8):
            program[i] = x
            for y in range(8):
                program[j] = y
                for z in range(8):
                    program[k] = z
                    yield tuple(program)

    used = [False]*len(instructions)
    sequence = []
    def Generate():
        if len(sequence) == len(instructions):
            template = tuple(v for i in sequence for v in instructions[i])
            yield from GeneratePrograms(template)
            return

        unblocked = [i for i, b in enumerate(blockers) if not used[i] and not b]
        assert unblocked
        for i in unblocked:
            used[i] = True
            for j in blocking[i]:
                blockers[j].remove(i)

            sequence.append(i)
            yield from Generate()
            sequence.pop()

            used[i] = False
            for j in blocking[i]:
                blockers[j].add(i)

    yield from Generate()


def Run(A, B=0, C=0):
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


def SolveBackward(A, i):
    if i == 0: return A
    return min((SolveBackward((A << 3) + x, i - 1) for x in range(i == len(program), 8)
            if DecodeOne((A << 3) + x) == program[i - 1]), default=inf)


if __name__ == '__main__':
    min_ans, max_ans = inf, -1
    for program in sorted(GenerateAllPrograms()):
        ans = SolveBackward(0, len(program))
        if ans < inf:
            min_ans = min(min_ans, ans)
            max_ans = max(max_ans, ans)
            print(','.join(map(str, program)), ans)
    print('Minimum possible answer:', min_ans, file=sys.stderr)
    print('Maximum possible answer:', max_ans, file=sys.stderr)
