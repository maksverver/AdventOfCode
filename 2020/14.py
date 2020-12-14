import re
import sys

def interpret(mask, ones):
    return int(''.join('01'[ch in ones] for ch in mask), 2)

def submasks(template):
    mask = template
    masks = [mask]
    while mask:
        mask = (mask - 1) & template
        masks.append(mask)
    return masks

class Machine1:
    def __init__(self):
        self.mem = {}
        self.mask = None
        self.ones = None

    def set_mask(self, mask):
        self.mask = interpret(mask, 'X')
        self.ones = interpret(mask, '1')

    def store(self, addr, value):
        self.mem[addr] = value & self.mask | self.ones

class Machine2:
    def __init__(self):
        self.mem = {}
        self.mask = None
        self.ones = None
        self.floating = None

    def set_mask(self, mask):
        self.mask = interpret(mask, '0')
        self.ones = interpret(mask, '1')
        self.floating = submasks(interpret(mask, 'X'))

    def store(self, addr, value):
        addr = addr & self.mask | self.ones
        for ones in self.floating:
            self.mem[addr | ones] = value

m1 = Machine1()
m2 = Machine2()
for line in sys.stdin:
    m = re.match('mask = ([01X]*)\n', line)
    if m:
        m1.set_mask(m.group(1))
        m2.set_mask(m.group(1))
        continue
    m = re.match('mem\[(\d+)] = (\d+)\n', line)
    if m:
        m1.store(int(m.group(1)), int(m.group(2)))
        m2.store(int(m.group(1)), int(m.group(2)))
        continue
    print('Unparsable line: "%s"' % line.strip(), file=sys.stderr)
    assert False
print(sum(m1.mem.values()))
print(sum(m2.mem.values()))
