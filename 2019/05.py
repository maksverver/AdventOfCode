from intcode import ReadInts, RunMachine

ints = ReadInts()

# Part 1
outputs = RunMachine(ints, [1])
assert all(x == 0 for x in outputs[:-1])
print(outputs[-1])

# Part 2
output, = RunMachine(ints, [5])
print(output)
