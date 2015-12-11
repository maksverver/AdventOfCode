import sys

total = 0
for line in sys.stdin:
	l,w,h = map(int, line.split('x'))
	sides = [l*w, w*h, h*l]
	sides.sort()
	a,b,c = sides
	total += 3*a + 2*b + 2*c
print total
