from math import lcm
from operator import add, mul
import re
import sys

class Base3:
  def __init__(self, value):
    self.digits = [value]
    self.Normalize()

  def DivideBy3(self):
    d = self.digits.pop(0)
    if not self.digits:
      self.digits.append(0)
    return d

  def AddInt(self, value):
    assert isinstance(value, int) and value >= 0
    self.digits[0] += value
    self.Normalize()

  def Normalize(self):
    carry = 0
    digits = self.digits
    while len(digits) > mod3len:
      digits.pop()
    for i, d in enumerate(digits):
      d += carry
      carry = d // 3
      d %= 3
      digits[i] = d
      if carry == 0: break
    while carry > 0 and len(digits) < mod3len:
      digits.append(carry % 3)
      carry //= 3

  def NormalizeAll(self):
    carry = 0
    digits = self.digits
    while len(digits) > mod3len:
      digits.pop()
    for i, d in enumerate(digits):
      d += carry
      carry = d // 3
      d %= 3
      digits[i] = d
    while carry > 0 and len(digits) < mod3len:
      digits.append(carry % 3)
      carry //= 3

  def AddBase3(self, o):
    assert self == o
    digits = self.digits
    for i, d in enumerate(digits):
      digits[i] = 2 * d
    self.NormalizeAll()

  def MulInt(self, value):
    digits = self.digits
    for i, d in enumerate(self.digits):
      digits[i] = d * value
    self.NormalizeAll()

  def MulBase3(self, o):
    assert self == o
    digits = self.digits
    new_digits = [0]*min(len(digits) * 2 - 1, mod3len)
    for i, x in enumerate(digits):
      if i == mod3len:
        break
      for j, y in enumerate(digits):
        if i + j == mod3len:
          break
        new_digits[i + j] += x * y
    self.digits = new_digits
    self.NormalizeAll()

  def IntValue(self):
    res = 0
    mul = 1
    for d in self.digits:
      res += mul * d
      mul *= 3
    return res

  def __str__(self):
    return ''.join(map(str, reversed(self.digits)))


# for i in range(100):
#   val = Base3(i)
#   assert int(str(val), 3) == i

#   for j in range(100):
#     val = Base3(i)
#     val.AddInt(j)
#     assert int(str(val), 3) ==  i + j

#     val = Base3(i)
#     val.MulInt(j)
#     assert int(str(val), 3) ==  i * j

#   val = Base3(i)
#   val.AddBase3(val)
#   assert int(str(val), 3) ==  i + i

#   val = Base3(i)
#   val.MulBase3(val)
#   assert int(str(val), 3) ==  i * i


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


  global mod3len
  mod3len = rounds * len(monkey_defs)


  monkeys = []
  for def_ in monkey_defs:
    monkeys.append(Monkey(def_, monkeys))

  #PrintMonkeys(monkeys)
  inspected = [0]*len(monkeys)
  for r in range(rounds):

    # The exponent needs to be the maximum number of times an item
    # is inspected, which should be bounded by 20 * num_monkeys,
    # altough we can probably reduce this somehwat.
    mod3len = max((rounds - r) * len(monkey_defs))

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

print(Solve(20))
