import sys

grid = [ [ False for _ in range(1000) ] for _ in range(1000) ]

def turn_on(v): return v + 1
def turn_off(v): return max(v - 1, 0)
def toggle(v): return v + 2

def update(f, r1, c1, r2, c2):
	for r in range(r1, r2 + 1):
		for c in range(c1, c2 + 1):
			grid[r][c] = f(grid[r][c])

def parse_coords(s):
	return map(int, s.split(','))

def parse_rect(s, t):
	r1,c1 = parse_coords(s)
	r2,c2 = parse_coords(t)
	assert r1 <= r2 and c1 <= c2
	return (r1, c1, r2, c2)

for line in sys.stdin:
	words = line.split()
	if words[0] == 'turn':
		assert words[3] == 'through'
		if words[1] == 'on':
			update(turn_on, *parse_rect(words[2], words[4]))
		elif words[1] == 'off':
			update(turn_off, *parse_rect(words[2], words[4]))
		else:
			assert False
	elif words[0] == 'toggle':
		assert words[2] == 'through'
		update(toggle, *parse_rect(words[1], words[3]))
	else:
		assert False

print sum(map(sum, grid))
