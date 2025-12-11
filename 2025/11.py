from functools import cache
import sys

outputs = {}
for line in sys.stdin:
    src, dsts = line.strip().split(': ')
    outputs[src] = dsts.split()

def CountPaths1(v='you'):
    if v == 'out':
        return 1
    return sum(CountPaths1(w) for w in outputs[v])

@cache
def CountPaths2(v='svr', dac=False, fft=False):
    if v == 'out':
        return dac and fft
    dac |= v == 'dac'
    fft |= v == 'fft'
    return sum(CountPaths2(w, dac, fft) for w in outputs[v])

print(CountPaths1())  # part 1
print(CountPaths2())  # part 2
