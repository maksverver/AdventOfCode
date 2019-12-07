from intcode import Machine, MachineState
from itertools import permutations
import sys

ints = list(map(int, sys.stdin.readline().split(',')))

def CalculateOutputSignal(phases):
    machines = []
    for phase in phases:
        machine = Machine(ints)
        machine.PutInput(phase)
        machines.append(machine)
    machines[0].PutInput(0)
    last_output = None
    while True:
        all_halted = True
        all_blocked = True
        for i, machine in enumerate(machines):
            state = machine.Run()
            if state == MachineState.HALT:
                continue
            all_halted = False
            if state == MachineState.INPUT:
                continue
            all_blocked = False
            if state == MachineState.OUTPUT:
                output = machine.GetOutput()
                if i + 1 < len(machines):
                    machines[i + 1].PutInput(output)
                else:
                    machines[0].PutInput(output)
                    last_output = output
        if all_halted:
            break
        assert not all_blocked
    return last_output

print(max(CalculateOutputSignal(phases) for phases in permutations(range(5, 10))))
