import sys

# Read initial wire values (not used by this script)
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

shapes = {
    'AND': 'rectangle',
    'XOR': 'oval',
    'OR':  'diamond',
}
colors = {
    'AND': 'tomato',
    'XOR': 'lime',
    'OR':  'orange',
}

print('digraph {')
print('rankdir=LR')
print('node [style=filled fillcolor=cyan]')
for c, (op, a, b) in ports.items():
    print(f'{c} [label="{c} = {a} {op} b" shape={shapes[op]} fillcolor={colors[op]}]')
    print(f'{a} -> {c}')
    print(f'{b} -> {c}')
print('}')
