from itertools import izip, count
import re
import sys

def gen_coords():
	for diagonal in count(1):
		for n in xrange(diagonal):
			yield diagonal - n, 1 + n

def gen_codes():
	code = 20151125
	while True:
		yield code
		code = code * 252533 % 33554393

for line in sys.stdin:
	row, col = map(int, re.findall('\d+', line))
	for coords, code in izip(gen_coords(), gen_codes()):
		if coords == (row, col):
			print code
			break
