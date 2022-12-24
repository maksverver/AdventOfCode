from operator import add, sub, mul
import sys

def Div(a, b):
  assert a % b == 0
  return a // b

OPS = {'+': add, '-': sub, '*': mul, '/': Div}

monkeys = {}

memo = {}

def Fetch(label):
  if label not in memo:
    memo[label] = monkeys[label]()
  return memo[label]

def MakeLiteral(value):
  return lambda: value

def MakeExpression(a, op, b):
  return lambda: op(Fetch(a), Fetch(b))

for line in sys.stdin:
  label, rest = line.strip().split(': ')
  if rest[0].isalpha():
    a, op, b = rest.split()
    monkey = MakeExpression(a, OPS[op], b)
  else:
    monkey = MakeLiteral(int(rest))
  monkeys[label] = monkey

print(Fetch('root'))

