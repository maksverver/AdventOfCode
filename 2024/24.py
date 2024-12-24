from collections import defaultdict
from random import randrange
import sys


def ParseInput(f=sys.stdin):
    # Read initial wire values (only used for part 1)
    inputs = {}
    for line in sys.stdin:
        line = line.strip()
        if not line: break
        key, val = line.split(': ')
        assert key not in inputs
        inputs[key] = int(val)

    # For each line "a OP b -> c", ports[c] = (OP, a, b)
    ports = {}
    for line in sys.stdin:
        line = line.strip()
        expr, c = line.split(' -> ')
        a, op, b = expr.split()
        assert c not in ports and c not in inputs
        ports[c] = (op, a, b)

    assert set(inputs) & set(ports) == set()

    return inputs, ports


# Evaluates the circuit consisting of the given ports and with the given inputs.
#
# Returns an integer corresponding with the bits of the z-wires, or None if a
# cycle was detected in the input ports (which can happen after swapping the
# wrong wires).
def Evaluate(inputs, ports):
    dependencies = defaultdict(set)
    dependants = defaultdict(set)
    for c, (op, a, b) in ports.items():
        assert c not in dependencies
        for d in (a, b):
            if d not in inputs:
                dependencies[c].add(d)
                dependants[d].add(c)

    operations = {
        'AND': lambda x, y: x & y,
        'OR':  lambda x, y: x | y,
        'XOR': lambda x, y: x ^ y,
    }

    # Evaluate ports in topological order
    answer = 0
    values = dict(inputs)
    todo = []
    for c in ports:
        if not dependencies[c]:
            todo.append(c)

    for c in todo:
        assert not dependencies[c]
        op, a, b = ports[c]
        values[c] = operations[op](values[a], values[b])
        for d in dependants[c]:
            dependencies[d].remove(c)
            if not dependencies[d]:
                todo.append(d)

    if len(todo) == len(ports):
        # Reconstruct integer output from binary z00 wires
        return sum(values[c] << int(c[1:]) for c in values if c.startswith('z'))

    return None  # Cycle detected in ports graph!


# Calculates how many of the lower bits are added correctly by the circuit
# described by `ports`.
#
# This is a probabilistic algorithm that performs up to `trials` independent
# trials to confirm the answer.
#
# If `lower_bound` is set, this function will return an exact answer only if it
# is greater than `lower_bound`. This allows bailing out early when a pair of
# operands is found that has an error in a bit at or below `lower_bound`, which
# greatly speeds up the computation.
def CalculateCorrectBits(ports, lower_bound=0, trials=1000):
    answer = 46
    for trial in range(trials):
        x = randrange(0, 2**45)
        y = randrange(0, 2**45)
        z = x + y
        r = Evaluate(MakeInputs(x, y), ports)
        if r is None:
            return 0  # invalid circuit that contains a cycle
        if z != r:
            errors = z ^ r
            answer = min(answer, (errors & -errors).bit_length() - 1)
        if answer <= lower_bound:
            break
    return answer


def MakeInputs(x, y):
    assert 0 <= x < 2**45
    assert 0 <= y < 2**45
    inputs = {}
    for i in range(45):
        inputs[f'x{i:02}'] = (x >> i) & 1
        inputs[f'y{i:02}'] = (y >> i) & 1
    return inputs


def MakePorts(ports, swaps):
    res = dict(ports)
    for c, d in swaps:
        res[c], res[d] = res[d], res[c]
    return res


def flattened(iterable_of_iterables):
    return (element for iterable in iterable_of_iterables for element in iterable)


if __name__ == '__main__':

    # Read input
    inputs, ports = ParseInput()

    # Part 1: evaluate circuit with the given inputs
    print(Evaluate(inputs, ports))

    # Part 2: figure out which wires to swap to fix the addition circuit.
    #
    # The addition circuit is a connected sequence of adders, one per bit.
    # Logically the higher bits should not be able to affect the lower bits,
    # so can fix each bit in sequence.
    #
    # The code below assumes that we can fix each adder with a single swap (it
    # could be extended to support two or more swaps, but it would become
    # increasingly expensive). For every possible swap it runs
    # CalculateCorrectBits() to see if the solution has improved.
    swaps = []
    next_bit = CalculateCorrectBits(ports)
    while next_bit < 46:
        print(f'Fixing adder {next_bit}...', file=sys.stderr)

        wires_available = set(ports) - set(flattened(swaps))
        for swap in ((c, d) for c in wires_available for d in wires_available if c < d):
            n = CalculateCorrectBits(MakePorts(ports, swaps + [swap]), next_bit)
            if n > next_bit:
                next_bit = n
                swaps.append(swap)
                break
        else:
            print(f'No improvement found for bit {next_bit}')
            sys.exit(1)

    # Print swapped wires as sorted comma-separated strings
    print(','.join(sorted(flattened(swaps))))
