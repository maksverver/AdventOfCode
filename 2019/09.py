from intcode import ReadInts, RunMachine

ints = ReadInts()

print(*RunMachine(ints, [1]))  # Part 1
print(*RunMachine(ints, [2]))  # Part 2
