from intcode import ReadInts, RunMachine
from itertools import permutations

ints = ReadInts()

def CalculateOutputSignal(phases):
    signal = 0
    for phase in phases:
        signal, = RunMachine(ints, [phase, signal])
    return signal

print(max(CalculateOutputSignal(phases) for phases in permutations(range(5))))
