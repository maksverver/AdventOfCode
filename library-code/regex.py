import re

line = '123 + 456 = 789'  # example


# Extract all numbers, ignoring other characters. This is often sufficient.
a, b, c = map(int, re.findall(r'\d+', line))

assert (a, b, c) == (123, 456, 789)


# Exact matching of separators. This is sometimes necessary and often useful as
# a sanity check. Using re.match() is also useful when it's not guaranteed that
# a pattern matches a line.
PATTERN = re.compile(r'^(\d+) \+ (\d+) = (\d+)$')

if m := re.match(PATTERN, line):
  a, b, c = map(int, m.groups())
  assert (a, b, c) == (123, 456, 789)
else:
  print('No match!')
  assert False
