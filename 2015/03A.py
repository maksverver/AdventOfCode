import sys

visited = set([(0, 0)])
x = y = 0
for c in sys.stdin.read():
	if c == '>':
		x += 1
	elif c == '<':
		x -= 1
	elif c == '^':
		y += 1
	elif c == 'v':
		y -= 1
	visited.add((x, y))
print(len(visited))
