import sys

for line in sys.stdin:
	answer = None
	level = 0
	for i, c in enumerate(line):
		if c == '(':
			level += 1
		elif c == ')':
			level -= 1
			if level < 0:
				answer = i
				break
	print answer + 1
