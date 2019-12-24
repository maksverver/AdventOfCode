from intcode import ReadInts, MachineState, Machine

ints = ReadInts()

def MakeMachine(i):
    machine = Machine(ints)
    machine.PutInput(i)
    return (machine, [], [])

machines = [MakeMachine(i) for i in range(50)]
answer = None
while answer is None:
    for machine, inputs, outputs in machines:
        state = machine.Run()
        if state == MachineState.INPUT:
            if inputs == []:
                machine.PutInput(-1)
            else:
                x, y = inputs[0]
                del inputs[0]
                machine.PutInput(x)
                machine.PutInput(y)
        elif state == MachineState.OUTPUT:
            outputs.append(machine.GetOutput())
            if len(outputs) >= 3:
                dest, x, y = outputs[:3]
                del outputs[:3]
                if dest == 255:
                    answer = y
                    break
                assert 0 <= dest < len(machines)
                machines[dest][1].append((x, y))
        else:
            print('Machine reached unexpected state', state)
            assert False

print(answer)
