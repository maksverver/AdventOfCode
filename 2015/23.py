import sys

def hlf(r):
	def apply(regs):
		regs[r] //= 2
		regs['ip'] += 1
	return apply

def tpl(r):
	def apply(regs):
		regs[r] *= 3
		regs['ip'] += 1
	return apply

def inc(r):
	def apply(regs):
		regs[r] += 1
		regs['ip'] += 1
	return apply

def jmp(offset):
	def apply(regs):
		regs['ip'] += offset
	return apply

def jie(r, offset):
	def apply(regs):
		regs['ip'] += offset if regs[r]%2 == 0 else 1
	return apply

def jio(r, offset):
	def apply(regs):
		regs['ip'] += offset if regs[r] == 1 else 1
	return apply

def parse(line):
	opcode, args = line.strip().split(' ', 1)
	args = args.split(', ')
	if opcode == 'hlf':
		r, = args
		return hlf(r)
	if opcode == 'tpl':
		r, = args
		return tpl(r)
	if opcode == 'inc':
		r, = args
		return inc(r)
	if opcode == 'jmp':
		offset, = args
		return jmp(int(offset))
	if opcode == 'jie':
		r, offset = args
		return jie(r, int(offset))
	if opcode == 'jio':
		r, offset = args
		return jio(r, int(offset))

def execute(instructions, regs):
	while 0 <= regs['ip'] < len(instructions):
		instructions[regs['ip']](regs)

instructions = list(map(parse, sys.stdin))

# Part 1
regs = {'ip': 0, 'a': 0, 'b': 0}
execute(instructions, regs)
print(regs['b'])

# Part 2
regs = {'ip': 0, 'a': 1, 'b': 0}
execute(instructions, regs)
print(regs['b'])
