import sys

class InvalidOutputException(Exception):
  pass

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
    return ip + (loady(regs) if loadx(regs) else 1)
  return execute

def GenCpy(x, y):
  loadx = GenLoad(x)
  def execute(ip, regs):
    regs[y] = loadx(regs)
    return ip + 1
  return execute

def GenOut(x):
  loadx = GenLoad(x)
  def execute(ip, regs):
    if loadx(regs) != regs['out']:
      raise InvalidOutputException()
    regs['out'] ^= 1
    return ip + 1
  return execute

def Parse(line):
  opcode, args = line.split(None, 1)
  args = args.split()
  if opcode == 'inc': return GenInc(*args)
  if opcode == 'dec': return GenDec(*args)
  if opcode == 'jnz': return GenJnz(*args)
  if opcode == 'cpy': return GenCpy(*args)
  if opcode == 'out': return GenOut(*args)

def Run(regs, ip = 0):
  seen = set()
  while True:
    # Detect loops. For performance, we don't check on every instruction, but
    # instead use the fixed address of an infinitely-recurring instruction (in
    # this case, the address of the `out` instruction).
    if ip == 28:
      key = tuple(regs.items())
      if key in seen:
        break
      seen.add(key)

    # Execute next instruction
    assert 0 <= ip < len(instructions)
    ip = instructions[ip](ip, regs)
  return regs

instructions = map(Parse, sys.stdin)
a = 0
while True:
  try:
    Run({'a': a, 'b': 0, 'c': 0, 'd': 0, 'out': 0})
    break
  except InvalidOutputException:
    a += 1
print a
