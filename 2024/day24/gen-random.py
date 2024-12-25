from random import choice, randint, randrange, sample, shuffle
from solve import Evaluate, MakePorts
import sys

possible_swaps = ()

nodes = set()

def NewNode():
    alphabet = 'abcdefghijklmnopqrstuvw'
    while True:
        node = choice(alphabet) + choice(alphabet) + choice(alphabet)
        if node not in nodes:
            nodes.add(node)
            return node

ops = {}

def DefineOp(a, op, b, c):
    assert c not in ops
    ops[c] = (op, a, b)
    return c

def NodeX(i): return f'x{i:02}'
def NodeY(i): return f'y{i:02}'
def NodeZ(i): return f'z{i:02}'

def MakeFirst(x, y, z, carry_out):
    DefineOp(x, 'XOR', y, z)
    DefineOp(x, 'AND', y, carry_out)

def MakeIntermediate(x, y, z, carry_in, carry_out):
    xor1 = DefineOp(x, 'XOR', y, NewNode())
    and1 = DefineOp(x, 'AND', y, NewNode())
    DefineOp(carry_in, 'XOR', xor1, z)
    and2 = DefineOp(xor1, 'AND', carry_in, NewNode())
    DefineOp(and1, 'OR', and2, carry_out)

input_bits = 45

def MakeInputs(x, y):
    inputs = {}
    for i in range(input_bits):
        inputs[NodeX(i)] = (x >> i) & 1
        inputs[NodeY(i)] = (y >> i) & 1
    return inputs

input_x = randrange(0, 2**input_bits)
input_y = randrange(0, 2**input_bits)
initial_wires = MakeInputs(input_x, input_y)

all_nodes = set()
per_bit_nodes = []

carry_in = None
for bit in range(input_bits):
    carry_out = NewNode() if bit + 1 < input_bits else NodeZ(bit + 1)
    if carry_in is None:
        MakeFirst(NodeX(bit), NodeY(bit), NodeZ(bit), carry_out)
    else:
        MakeIntermediate(NodeX(bit), NodeY(bit), NodeZ(bit), carry_in, carry_out)
    carry_in = carry_out

    new_all_nodes = set(ops.keys())
    per_bit_nodes.append(new_all_nodes - all_nodes)
    all_nodes = new_all_nodes
assert carry_out == NodeZ(input_bits)

def MakeSwappedOps():
    while True:
        new_ops = dict(ops)
        swaps = []
        for nodes in sample(sorted(per_bit_nodes), k=4):
            a, b = sample(sorted(nodes), k=2)
            new_ops[a], new_ops[b] = new_ops[b], new_ops[a]
            swaps += [a, b]
        if Evaluate(initial_wires, new_ops) is not None:
            return new_ops, swaps


def WriteGraph(ops, filename):
    with open(filename, 'wt') as f:
        # Generate graphviz output
        print('digraph {', file=f)
        print('rankdir=LR', file=f)
        for c, (op, a, b) in ops.items():
            print(f'{c} [label="{c} = {a} {op} {b}"]', file=f)
            print(f'{a} -> {c}', file=f)
            print(f'{b} -> {c}', file=f)
        print('}', file=f)

def WriteInput(ops, filename):
    with open(filename, 'wt') as f:
        for k, v in sorted(initial_wires.items()):
            print(f'{k}: {v}', file=f)
        print(file=f)
        op_lines = [f'{a} {op} {b} -> {c}' for (c, (op, a, b)) in ops.items()]
        shuffle(op_lines)
        for line in op_lines:
            print(line, file=f)

new_ops, swaps = MakeSwappedOps()

WriteGraph(new_ops, 'test.gv')
WriteInput(new_ops, 'test.txt')

print(Evaluate(initial_wires, new_ops), file=sys.stderr)  # answer part 1
print(','.join(sorted(swaps)), file=sys.stderr)  # answer part 2
