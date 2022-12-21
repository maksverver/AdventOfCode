from operator import add, sub, mul
import sys

class Operator: pass


class AddOp(Operator):
  def Perform(self, a, b):
    return a + b

  def DetermineLeft(self, b, c):
    return c - b  #  a + b = c  ->  a = c - b

  def DetermineRight(self, a, c):
    return c - a  #  a + b = c  ->  b = c - a


class SubOp(Operator):
  def Perform(self, a, b):
    return a - b

  def DetermineLeft(self, b, c):
    return b + c  #  a - b = c  ->  a = b + c

  def DetermineRight(self, a, c):
    return a - c  #  a - b = c  ->  b = a - c


class MulOp(Operator):
  def Perform(self, a, b):
    return a * b

  def DetermineLeft(self, b, c):
    assert c % b == 0
    return c // b  #  a * b = c  ->  a = c / b

  def DetermineRight(self, a, c):
    assert c % a == 0
    return c // a  #  a * b = c  ->  b = c / a


class DivOp(Operator):
  def Perform(self, a, b):
    assert a % b == 0
    return a // b

  def DetermineLeft(self, b, c):
    return b * c  #  a / b = c  ->  a = b * c

  def DetermineRight(self, a, c):
    assert a % c == 0
    return a // c  #  a / b = c  ->  b = a / c


OPS = {'+': AddOp(), '-': SubOp(), '*': MulOp(), '/': DivOp()}

# Some quick operator tests.
for a in range(1, 11):
  for b in range(1, 11):
    for op in OPS.values():
      if not isinstance(op, DivOp) or a % b == 0:
        c = op.Perform(a, b)
        assert op.DetermineLeft(b, c) == a
        assert op.DetermineRight(a, c) == b


class Expr: pass


class LitExpr(Expr):
  def __init__(self, value):
    self.value = value

  def Evaluate(self):
    return self.value


class BinExpr(Expr):
  def __init__(self, lhs, op, rhs):
    self.lhs = lhs
    self.op = op
    self.rhs = rhs
    self.arg1 = None
    self.arg2 = None
    self.value = None
    self.evaluated = False

  def Evaluate(self):
    if not self.evaluated:
      self.arg1 = a = self.lhs.Evaluate()
      self.arg2 = b = self.rhs.Evaluate()
      self.value = None if a is None or b is None else self.op.Perform(a, b)
      self.evaluated = True
    return self.value

  def DetermineUnknown(self, result):
    assert (self.arg1 is None) != (self.arg2 is None)
    if self.arg1 is None:
      return self.lhs.DetermineUnknown(self.op.DetermineLeft(self.arg2, result))
    else:
      return self.rhs.DetermineUnknown(self.op.DetermineRight(self.arg1, result))


class IndeterminateExpr(Expr):
  def Evaluate(self):
    return None

  def DetermineUnknown(self, result):
    return result


def ReadInput(file=sys.stdin):
  definitions = {}
  for line in file:
    label, rest = line.strip().split(': ')
    if rest[0].isalpha():
      lhs, op, rhs = rest.split()
      definitions[label] = (lhs, OPS[op], rhs)
    else:
      definitions[label] = int(rest)
  return definitions


# Monkey label -> int or tuple (label1, operator, label2)
definitions = ReadInput()


# This supports arbitrary acyclic graphs of expressions, though in the official
# input for this problem, the expression graph is just a tree.
def MakeExpression(label, memo):
  result = memo.get(label)
  if result is None:
    d = definitions[label]
    if isinstance(d, int):
      result = LitExpr(d)
    else:
      lhs, op, rhs = d
      result = BinExpr(MakeExpression(lhs, memo), op, MakeExpression(rhs, memo))
    memo[label] = result
  return result


def SolvePart1():
  root = MakeExpression('root', {})
  return root.Evaluate()


def SolvePart2():
  root = MakeExpression('root', {'humn': IndeterminateExpr()})
  a = root.lhs.Evaluate()
  b = root.rhs.Evaluate()
  assert (a is None) != (b is None)
  if a is None:
    return root.lhs.DetermineUnknown(b)
  else:
    return root.rhs.DetermineUnknown(a)


ReadInput(sys.stdin)
print(SolvePart1())
print(SolvePart2())
