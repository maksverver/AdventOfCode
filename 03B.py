import sys

visited = set([(0, 0)])

def process(instructions):
	x = y = 0
	for c in instructions:
		if c == '>':
			x += 1
		elif c == '<':
			x -= 1
		elif c == '^':
			y += 1
		elif c == 'v':
			y -= 1
		visited.add((x, y))

# Note: this assumes the input contains ONLY valid instructions, and no other
# characters!
instructions = sys.stdin.read()
process(instructions[0::2])
process(instructions[1::2])
print len(visited)
