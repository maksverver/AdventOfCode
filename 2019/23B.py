from intcode import ReadInts, MachineState, Machine

ints = ReadInts()

def MakeMachine(i):
    machine = Machine(ints)
    machine.PutInput(i)
    return (machine, [], [])

machines = [MakeMachine(i) for i in range(50)]
last_nat_y = None
while True:
    nat_x = nat_y = None
    idle_cycles = 0
    while idle_cycles < 10:
        idle_cycles += 1
        for i, (machine, inputs, outputs) in enumerate(machines):
            state = machine.Run()
            if state == MachineState.INPUT:
                if inputs == []:
                    machine.PutInput(-1)
                else:
                    idle_cycles = 0
                    x, y = inputs[0]
                    del inputs[0]
                    machine.PutInput(x)
                    machine.PutInput(y)
            elif state == MachineState.OUTPUT:
                idle_cycles = 0
                outputs.append(machine.GetOutput())
                if len(outputs) >= 3:
                    dest, x, y = outputs[:3]
                    del outputs[:3]
                    if dest == 255:
                        nat_x = x
                        nat_y = y
                    else:
                        assert 0 <= dest < len(machines)
                        machines[dest][1].append((x, y))
            else:
                print('Machine reached unexpected state', state)
                assert False
    if nat_y == last_nat_y:
        break
    last_nat_y = nat_y
    machines[0][1].append((nat_x, nat_y))

print(last_nat_y)
