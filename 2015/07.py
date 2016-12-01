import sys

values = {}
cache = {}

def Eval(x):
	if x.isdigit():
		return int(x, 10)
	else:
		return values[x]()

def Copy(x): return lambda: Eval(x)
def Not(x): return lambda: ~Eval(x) & 0xffff
def And(x, y): return lambda: Eval(x) & Eval(y)
def Or(x, y): return lambda: Eval(x) | Eval(y)
def Lshift(x, y): return lambda: (Eval(x) << Eval(y)) & 0xffff
def Rshift(x, y): return lambda: Eval(x) >> Eval(y)

computing = []
def Assign(var, func):
	def Calc():
		if var not in cache:
			assert var not in computing  # cycle detect!
			computing.append(var)
			cache[var] = func()
			assert computing.pop() == var
		return cache[var]
	values[var] = Calc

for line in sys.stdin:
	parts = line.split()
	if len(parts) == 3:
		x, sep, r = parts
		assert sep == '->'
		Assign(r, Copy(x))
	elif len(parts) == 4:
		op, x, sep, r = parts
		assert sep == '->'
		if op == 'NOT': Assign(r, Not(x))
		else: assert False
	elif len(parts) == 5:
		x, op, y, sep, r = parts
		assert sep == '->'
		if op == 'AND': Assign(r, And(x, y))
		elif op == 'OR': Assign(r, Or(x, y))
		elif op == 'LSHIFT': Assign(r, Lshift(x, y))
		elif op == 'RSHIFT': Assign(r, Rshift(x, y))
		else:
			print op
			assert False
	else:
		print parts
		assert False

# Part 1
print(Eval('a'))

# Part 2
Assign('b', Copy(str(Eval('a'))))
cache = {}
print(Eval('a'))
