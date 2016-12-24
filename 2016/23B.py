import sys

regs = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
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

def Mul(a, b):
	Store(b, Load(a)*Load(b))

def Tgl(a):
	i = ip - 1 + Load(a)
	if 0 <= i < len(instrs):
		assert i >= 10  # otherwise optimization for part 2 doesn't work
		if len(instrs[i][1]) == 1:
			instrs[i][0] = 'dec' if instrs[i][0] == 'inc' else 'inc'
		elif len(instrs[i][1]) == 2:
			instrs[i][0] = 'cpy' if instrs[i][0] == 'jnz' else 'jnz'
		else:
			assert False

def Jnz(a, b):
	global ip
	def Move(src, dst):
		assert src != dst
		Store(dst, Load(src, dst))
		Store(src, 0)
	if b == '-2':
		sop = instrs[ip - 2][0]
		src, = instrs[ip - 2][1][0]
		dop = instrs[ip - 3][0]
		dst, = instrs[ip - 3][1][0]
		if dst == a:
			src, dst = dst, src
			sop, dop = dop, sop
		if src == a and dst != a:
			#print 'Optimize!', sop, src, dop, dst
			if sop == dop:
				Store(dst, Load(dst) - Load(src))
			else:
				Store(dst, Load(dst) + Load(src))
			Store(src, 0)
			return
	if Load(a):
		ip += Load(b) - 1

funcs = {
	'inc': Inc,
	'dec': Dec,
	'cpy': Cpy,
	'jnz': Jnz,
	'mul': Mul,
	'tgl': Tgl,
} 

instrs = []
for line in sys.stdin:
	parts = line.split()
	instrs.append([parts[0], parts[1:]])
while 0 <= ip < len(instrs):
	if ip == 2:
		# Optimize multiplication for part 2
		regs['a'] = regs['a']*regs['b']
		ip = 10
		continue
	opcode, args = instrs[ip]
	ip += 1
	funcs[opcode](*args)
print regs['a']
