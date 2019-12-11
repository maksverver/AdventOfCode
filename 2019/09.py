from intcode import RunMachine
import sys

ints = list(map(int, sys.stdin.readline().split(',')))

print(*RunMachine(ints, [1]))  # Part 1
print(*RunMachine(ints, [2]))  # Part 2
