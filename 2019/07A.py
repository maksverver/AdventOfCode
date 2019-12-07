from intcode import RunMachine
from itertools import permutations
import sys

ints = list(map(int, sys.stdin.readline().split(',')))

def CalculateOutputSignal(phases):
    signal = 0
    for phase in phases:
        signal, = RunMachine(ints, [phase, signal])
    return signal

print(max(CalculateOutputSignal(phases) for phases in permutations(range(5))))
