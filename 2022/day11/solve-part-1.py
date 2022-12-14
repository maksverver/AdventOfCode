from math import lcm
from operator import add, mul
import re
import sys

class Base3:
  def __init__(self, value):
    assert isinstance(value, int)
    self.value = value % mod3k

  def DivideBy3(self):
    rem = self.value % 3
    self.value //= 3
    return rem

  def AddInt(self, i):
    self.value = (self.value + i) % mod3k

  def AddBase3(self, o):
    self.value = (self.value + o.value) % mod3k

  def MulInt(self, i):
    self.value = (self.value * i) % mod3k

  def MulBase3(self, o):
    self.value = (self.value * o.value) % mod3k

  def __str__(self):
    return str(self.value)



class Acc:
  def __init__(self, value, base3_value=None):
    if base3_value is None:
      base3_value = Base3(value)
    self.mod_value = value % mod
    self.base3_value = base3_value

  def ModAddDiv3(self, value):
    if isinstance(value, int):
      mod_value = (self.mod_value + value) % mod
      self.base3_value.AddInt(value)
    elif isinstance(value, Acc):
      assert value == self
      mod_value = (self.mod_value + value.mod_value) % mod
      self.base3_value.AddBase3(value.base3_value)
    else:
      assert False
    self.mod_value = ((mod_value - self.base3_value.DivideBy3()) * inv3) % mod
    return self

  def ModMulDiv3(self, value):
    if isinstance(value, int):
      mod_value = (self.mod_value * value) % mod
      self.base3_value.MulInt(value)
    elif isinstance(value, Acc):
      assert value == self
      mod_value = (self.mod_value * value.mod_value) % mod
      self.base3_value.MulBase3(value.base3_value)
    else:
      assert False
    self.mod_value = ((mod_value - self.base3_value.DivideBy3()) * inv3) % mod
    return self


  def Divides(self, div):
    #assert mod % div == 0
    return self.mod_value % div == 0

  def __str__(self):
    return "Acc{%s, %s}" % (self.mod_value, self.base3_value)

class MonkeyDef:
  '''Definition of a monkey. Constaints just the properties parsed from the
  input and is never modified afterwards. Can be used to initialize a Monkey.'''
  def __init__(self, items, update, div, pos, neg):
    self.items = items
    self.update = update
    self.div = div
    self.pos = pos
    self.neg = neg

class Monkey:
  '''Stateful monkey, that has a mutable list of items and knows how to play
  keep-away with other monkeys.'''
  def __init__(self, def_, monkeys):
    self.monkeys = monkeys

    # Start out with an initial list of items copied from the definition.
    self.items = list(map(Acc, def_.items))

    # Define the next-monkey function.
    div = def_.div
    pos = def_.pos
    neg = def_.neg
    self.nextMonkey = lambda i: pos if i.Divides(div) else neg

    # Define the item-update function which differs between part 1 and 2.
    self.update = def_.update

  def Play(self):
    for item in self.items:
      item = self.update(item)
      self.monkeys[self.nextMonkey(item)].items.append(item)
    self.items.clear()


OPS = {
  '+': lambda a, b: a.ModAddDiv3(b),
  '*': lambda a, b: a.ModMulDiv3(b),
}

def ParseUpdate(a, op, b):
  op = OPS[op]

  if a == 'old' and b == 'old':
    return lambda i: op(i, i)

  if a == 'old':
    b = int(b)
    return lambda i: op(i, b)

  assert False


def ParseMonkeyDef(index, lines):
  assert len(lines) == 6
  m0 = re.match('Monkey (\d+):', lines[0])
  m1 = re.match('  Starting items: (\d+(, \d+)*)', lines[1])
  m2 = re.match('  Operation: new = (old|\d+) ([+*]) (old|\d+)', lines[2])
  m3 = re.match('  Test: divisible by (\d+)', lines[3])
  m4 = re.match('    If true: throw to monkey (\d+)', lines[4])
  m5 = re.match('    If false: throw to monkey (\d+)', lines[5])
  assert index == int(m0[1])
  items = list(map(int, m1[1].split(', ')))
  update = ParseUpdate(m2[1], m2[2], m2[3])
  div = int(m3[1])
  pos = int(m4[1])
  neg = int(m5[1])
  assert pos != index and neg != index
  return MonkeyDef(items, update, div, pos, neg)


def PrintMonkeys(monkeys):
  for i, m in enumerate(monkeys):
    print('Monkey {}: {}'.format(i, ', '.join(map(str, m.items))))
  print()


def Solve(rounds):
  global mod3k
  mod3k = 3**(rounds  * max_moves_per_round)

  monkeys = []
  for def_ in monkey_defs:
    monkeys.append(Monkey(def_, monkeys))

  #PrintMonkeys(monkeys)
  inspected = [0]*len(monkeys)
  for r in range(rounds):
    # Lower modulo to account for fewer rounds remaining
    mod3k = 3**((rounds - r) * max_moves_per_round)

    for i, m in enumerate(monkeys):
      inspected[i] += len(m.items)
      m.Play()
    #PrintMonkeys(monkeys)

  return mul(*sorted(inspected)[-2:])


def Inverse(a):
  '''Computes the multiplicative inverse of `a` modulo `mod`, assuming `a` and `mod` are coprime.'''
  # Extended Euclidean algorithm
  old_r, r = a, mod
  old_s, s = 1, 0
  old_t, t = 0, 1
  while r != 0:
    q = old_r // r
    old_r, r = r, old_r - q * r
    old_s, s = s, old_s - q * s
    old_t, t = t, old_t - q * t
  assert old_r == 1
  return old_s

monkey_defs = [ParseMonkeyDef(i, part.splitlines())
    for i, part in enumerate(sys.stdin.read().split('\n\n'))]

mod = lcm(*(m.div for m in monkey_defs))
assert mod % 3 != 0
inv3 = Inverse(3)
assert (inv3 * 3) % mod == 1

# Maximum number of times an item can move in a single round.
max_moves = [None]*len(monkey_defs)
for i, m in reversed(list(enumerate(monkey_defs))):
  max_moves[i] = max([1] + [max_moves[j] + 1 for j in [m.pos, m.neg] if j > i])
max_moves_per_round = max(max_moves)

print(Solve(20))
