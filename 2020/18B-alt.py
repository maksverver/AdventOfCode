import sys

def Parse(tokens):
    stack = []
    pos = 0

    def ParseProductExpression():
        nonlocal pos
        ParseSumExpression()
        if tokens[pos] == '*':
            pos += 1
            ParseProductExpression()
            stack.append(stack.pop() * stack.pop())

    def ParseSumExpression():
        nonlocal pos
        ParseBaseExpression()
        if tokens[pos] == '+':
            pos += 1
            ParseSumExpression()
            stack.append(stack.pop() + stack.pop())
    
    def ParseBaseExpression():
        nonlocal pos
        t = tokens[pos]
        if t == '(':
            pos += 1
            ParseProductExpression()
            assert tokens[pos] == ')'
            pos += 1
        else:
            assert t.isdigit()
            stack.append(int(t))
            pos += 1

    ParseProductExpression()
    assert tokens[pos] == '$'
    
    result, = stack
    return result

print(sum(Parse([ch for ch in line if not ch.isspace()] + ['$']) for line in sys.stdin))
