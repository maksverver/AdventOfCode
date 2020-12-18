import sys

def Parse(line, precedence):
    """Parses the expression using Dijkstra's Shunting Yard algorithm and
       returns a list of operations in reverse Polish notation (RPN) where
       values are ints and operators are strings ('+' or '*')."""
    output = []
    stack = []
    for ch in line:
        if ch.isspace():
            continue
        # N.B. all integers are single digits in the input.
        if ch.isdigit():
            output.append(int(ch))
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            assert ch in '+*'
            while stack and stack[-1] != '(' and precedence[ch] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(ch)
    assert '(' not in stack
    while stack:
        output.append(stack.pop())
    return output

def Evaluate(rpn):
    """Evaluates a list of operations in reverse Polish notations.
       e.g. Evaluate([1,2,3,'*','+']) == 7."""
    stack = []
    for x in rpn:
        if isinstance(x, int):
            stack.append(x)
        else:
            rhs = stack.pop()
            lhs = stack.pop()
            if x == '+':
                stack.append(lhs + rhs)
            elif x == '*':
                stack.append(lhs * rhs)
            else:
                assert False
    result, = stack
    return result

lines = list(sys.stdin)
print(sum(Evaluate(Parse(line, {'+': 0, '*': 0})) for line in lines))
print(sum(Evaluate(Parse(line, {'+': 1, '*': 0})) for line in lines))
