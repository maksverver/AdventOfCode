from enum import Enum
import re
import sys

class BinOp:
    def __init__(self, f, s):
        self.f = f
        self.s = s

    def __call__(self, a, b):
        return self.f(a, b)

    def __str__(self):
        return self.s

BinOp.ADD = BinOp(lambda a, b: a + b, '+')
BinOp.MUL = BinOp(lambda a, b: a * b, '*')

class Expr:
    def Eval(self):
        raise "Unimplemented!"

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def Eval(self):
        return self.value

class BinExpr(Expr):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return '(' + str(self.lhs) + str(self.op) + str(self.rhs) + ')'

    def Eval(self):
        return self.op(self.lhs.Eval(), self.rhs.Eval())

def ParseExpr(line):
    backstack = []
    stack = []
    for ch in line:
        if ch.isspace():
            continue
        # N.B. all integers are single digits in the input.
        if ch.isdigit():
            stack.append(Literal(int(ch)))
        elif ch == '+':
            stack.append(BinOp.ADD)
        elif ch == '*':
            stack.append(BinOp.MUL)
        elif ch == '(':
            backstack.append(stack)
            stack = []
        elif ch == ')':
            expr, = stack
            assert isinstance(expr, Expr)
            stack = backstack.pop()
            stack.append(expr)
        else:
            print("Unexpected character", ch)
            assert False
        if len(stack) == 3:
            lhs, op, rhs = stack
            assert isinstance(lhs, Expr)
            assert isinstance(rhs, Expr)
            assert isinstance(op, BinOp)
            stack = [BinExpr(op, lhs, rhs)]

    assert len(backstack) == 0
    assert len(stack) == 1
    return stack[0]

print(sum(ParseExpr(line).Eval() for line in sys.stdin))
