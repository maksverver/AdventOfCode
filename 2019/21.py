from intcode import ReadInts, RunMachine

ints = ReadInts()

def Run(commands):
    input = [ord(ch) for line in commands.split('\n') for ch in line + '\n' if line and line[0] != ';']
    output = RunMachine(ints, input)
    #print(''.join(map(chr, output[:-1])))
    return output[-1]

# Part 1
#  
#  ABCD
# @.      ~A
#
# @?..#   ~B & ~C & D
#
# @##.#   A & B & ~C & D
#
# (Found by trial and error.)
print(Run('''\
NOT A J
OR B T
OR C T
NOT T T
AND D T
OR T J
NOT C T
AND A T
AND B T
AND D T
OR T J
WALK'''))

# Part 2
#
#  ABCDEFGHI
# @xxx#y??y
# 
# (~A | ~B | ~C) & D & (E | H)
#
# Rationale:
#
# If one of A/B/C is a hole, we must jump at some point, and it's better
# to jump sooner rather than later, except in cases like:
#
#   ABCDEFGHI
#  @##.#.##.###
# 
# ...where jumping to D would trap us. Checking that we can proceed at either E
# or H seems sufficient for this input.
#
# The general case is unsolvable with limit lookahead, because if have a sequence
# like:
#
#       x y x y x y x y x   x
#   @##.#.#.#.#.#.#.#.#.#...##
#   @##.#.#.#.#.#.#.#.#...####
#
# We don't know if we should jump on the `x` or `y` labelled squares.

print(Run('''\
OR A T
AND B T
AND C T
NOT T T
AND D T
OR E J
OR H J
AND T J
RUN'''))
