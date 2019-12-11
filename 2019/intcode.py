from collections import defaultdict
from enum import Enum
from operator import add, mul, lt, eq

def jit(cond, new_ip, cur_ip):
    return new_ip if cond != 0 else cur_ip

def jif(cond, new_ip, cur_ip):
    return new_ip if cond == 0 else cur_ip

class MachineState(Enum):
    RUN = 0
    INPUT = 1
    OUTPUT = 2
    HALT = 3

class Machine:

    def __init__(self, ints):
        self.ints = defaultdict(int, enumerate(ints))
        self.ip = 0
        self.relbase = 0
        self.inputs = []
        self.outputs = []
        self.opcode_map = {
            1: ('IIO', add),
            2: ('IIO', mul),
            3: ('O', self.GetInput),
            4: ('I', self.PutOutput),
            5: ('IIP', jit),
            6: ('IIP', jif),
            7: ('IIO', lt),
            8: ('IIO', eq),
            9: ('I', self.AdjustRelbase),
        }

    def PutInput(self, input):
        self.inputs.append(input)

    def GetInput(self):
        input = self.inputs[0]
        del self.inputs[0]
        return input

    def PutOutput(self, output):
        self.outputs.append(output)

    def GetOutput(self):
        output = self.outputs[0]
        del self.outputs[0]
        return output

    def AdjustRelbase(self, offset):
        self.relbase += offset

    def Step(self):
        assert self.ip >= 0
        rem = self.ints[self.ip]
        self.ip += 1
        opcode = rem % 100
        rem //= 100
        params, func = self.opcode_map[opcode]
        args = []
        dests = []
        update_ip = False
        for i, t in enumerate(params):
            if t == 'P':
                args.append(self.ip)
                update_ip = True
                break
            assert t in 'IO'
            mode = rem % 10
            rem //= 10
            operand = self.ints[self.ip]
            self.ip += 1
            if mode == 2:
                operand += self.relbase
                mode = 0
            if t == 'I':
                assert mode in (0, 1)
                if mode == 0:
                    arg = self.ints[operand]
                else:
                    arg = operand
                args.append(arg)
            else:
                assert mode == 0
                assert operand >= 0
                dests.append(operand)
        result = func(*args)
        if update_ip:
            assert dests == []
            self.ip = result
        for i in dests:
            self.ints[i] = result

    def Run(self):
        while True:
            opcode = self.ints[self.ip] % 100
            if opcode == 99:
                return MachineState.HALT
            if opcode == 3 and self.inputs == []:
                return MachineState.INPUT
            self.Step()
            if opcode == 4:
                return MachineState.OUTPUT

def RunMachine(ints, inputs):
    machine = Machine(ints)
    for input in inputs:
        machine.PutInput(input)
    outputs = []
    while True:
        state = machine.Run()
        if state == MachineState.OUTPUT:
            outputs.append(machine.GetOutput())
            continue
        assert state == MachineState.HALT
        return outputs
