import sys

regs = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
ip = 0

def Load(x):
	return regs[x] if x in regs else int(x)

def Store(r, v):
	assert r in regs
	regs[r] = v

def Inc(a):
	Store(a, Load(a) + 1)

def Dec(a):
	Store(a, Load(a) - 1)

def Cpy(a, b):
	Store(b, Load(a))

def Tgl(a):
	i = ip - 1 + Load(a)
	if 0 <= i < len(instrs):
		if len(instrs[i][1]) == 1:
			instrs[i][0] = 'dec' if instrs[i][0] == 'inc' else 'inc'
		elif len(instrs[i][1]) == 2:
			instrs[i][0] = 'cpy' if instrs[i][0] == 'jnz' else 'jnz'
		else:
			assert False

def Jnz(a, b):
	if Load(a):
		global ip
		ip += Load(b) - 1

funcs = {
	'inc': Inc,
	'dec': Dec,
	'cpy': Cpy,
	'jnz': Jnz,
	'tgl': Tgl,
}

instrs = []
for line in sys.stdin:
	parts = line.split()
	instrs.append([parts[0], parts[1:]])
while 0 <= ip < len(instrs):
	opcode, args = instrs[ip]
	ip += 1
	funcs[opcode](*args)
print(regs['a'])
