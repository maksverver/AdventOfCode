import sys

def GenLoad(x):
  if x.isalpha():
    return lambda regs: regs[x]
  else:
    i = int(x)
    return lambda regs: i

def GenInc(x):
  def execute(ip, regs):
    regs[x] += 1
    return ip + 1
  return execute

def GenDec(x):
  def execute(ip, regs):
    regs[x] -= 1
    return ip + 1
  return execute

def GenJnz(x, y):
  loadx = GenLoad(x)
  loady = GenLoad(y)
  def execute(ip, regs):
    if loadx(regs):
      return ip + loady(regs)
    else:
      return ip + 1
  return execute

def GenCpy(x, y):
  loadx = GenLoad(x)
  def execute(ip, regs):
    regs[y] = loadx(regs)
    return ip + 1
  return execute

def Parse(line):
  opcode, args = line.split(None, 1)
  args = args.split()
  if opcode == 'inc': return GenInc(*args)
  if opcode == 'dec': return GenDec(*args)
  if opcode == 'jnz': return GenJnz(*args)
  if opcode == 'cpy': return GenCpy(*args)

def Run(regs):
  ip = 0
  while 0 <= ip < len(instructions):
    ip = instructions[ip](ip, regs)
  return regs

instructions = list(map(Parse, sys.stdin))

# Part 1
print(Run({'a': 0, 'b': 0, 'c': 0, 'd': 0})['a'])

# Part 2
print(Run({'a': 0, 'b': 0, 'c': 1, 'd': 0})['a'])
