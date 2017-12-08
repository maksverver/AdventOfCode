from collections import defaultdict
import operator
import re
import sys

operators = {
  'inc': operator.add,
  'dec': operator.sub,
  '>': operator.gt,
  '<': operator.lt,
  '>=': operator.ge,
  '<=': operator.le,
  '==': operator.eq,
  '!=': operator.ne,
}

regs = defaultdict(lambda: 0)
max_value = 0
for line in sys.stdin:
  dst_reg, dst_op, dst_val, src_reg, src_op, src_val = \
      re.match(r'(\w+) (inc|dec) (-?\d+) if (\w+) (<|>|<=|>=|==|!=) (-?\d+)', line).groups()
  if operators[src_op](regs[src_reg], int(src_val)):
    new_value = regs[dst_reg] = operators[dst_op](regs[dst_reg], int(dst_val))
    max_value = max(max_value, new_value)

# Part 1: maximum value in a register at the end of the program.
print(max(regs.values()))

# Part 2: maximum value in a register at any point.
print(max_value)
