from math import lcm
from operator import add, mul
import re
import sys

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
  def __init__(self, def_, monkeys, mod, divAfterUpdate):
    self.monkeys = monkeys

    # Start out with an initial list of items copied from the definition.
    self.items = list(def_.items)

    # Define the next-monkey function.
    div = def_.div
    pos = def_.pos
    neg = def_.neg
    self.nextMonkey = lambda i: pos if i % div == 0 else neg

    # Define the item-update function which differs between part 1 and 2.
    update = def_.update
    if divAfterUpdate:
      # Part 1: divide by 3 after every update
      self.update = lambda i: update(i) // divAfterUpdate % mod
    else:
      # Part 2: reduce modulo `mod` after every update
      self.update = lambda i: update(i) % mod

  def Play(self):
    for item in self.items:
      old_item = item
      item = self.update(item)
      self.monkeys[self.nextMonkey(item)].items.append(item)
    self.items.clear()


OPS = {'+': add, '*': mul}

def ParseUpdate(a, op, b):
  op = OPS[op]

  if a == 'old' and b == 'old':
    def F(i):
      r = op(i, i)
      return r
    return F

  if a == 'old':
    b = int(b)
    def F(i):
      r = op(i, b)
      return r
    return F

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


def Solve(rounds, mod, div):
  monkeys = []
  for def_ in monkey_defs:
    monkeys.append(Monkey(def_, monkeys, mod, div))

  inspected = [0]*len(monkeys)
  for r in range(rounds):
    for i, m in enumerate(monkeys):
      inspected[i] += len(m.items)
      m.Play()

    if mod is None:
      for m in monkeys:
        if m.items:
          max_item = max(max_item, max(m.items))

  return mul(*sorted(inspected)[-2:])


monkey_defs = [ParseMonkeyDef(i, part.splitlines())
    for i, part in enumerate(sys.stdin.read().split('\n\n'))]

mod = lcm(*(m.div for m in monkey_defs))

# Maximum number of times an item can move in a single round.
max_moves = [None]*len(monkey_defs)
for i, m in reversed(list(enumerate(monkey_defs))):
  max_moves[i] = max([1] + [max_moves[j] + 1 for j in [m.pos, m.neg] if j > i])
max_moves_per_round = max(max_moves)

print(Solve(20, mod * 3**(20*max_moves_per_round), 3))
#print(Solve(10_000, mod, None))
