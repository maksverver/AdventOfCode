import sys

total = 0
for line in sys.stdin:
	a,b,c = sorted(map(int, line.split('x')))
	total += 2*(a + b) + a*b*c
print total
