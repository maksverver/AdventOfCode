import sys

colors = {
    'you': 'pink',
    'svr': 'lightblue',
    'dac': 'yellow',
    'fft': 'orange',
    'out': 'lightgreen',
}

print('digraph {')
for src, color in colors.items():
    print(f'{src} [fillcolor="{colors[src]}", style=filled];')

outputs = {}
for line in sys.stdin:
    src, dsts = line.strip().split(': ')
    outputs[src] = dsts.split()
    for dst in dsts.split():
        print(f'{src} -> {dst};')
print('}')
