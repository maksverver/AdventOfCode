import sys

for line in sys.stdin:
	print line.count('(') - line.count(')')
