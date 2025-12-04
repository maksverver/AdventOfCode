import sys

def is_nice(word):
	vowels = 0
	doubles = 0
	b = '~'
	for c in word:
		vowels += (c in 'aoeui')
		doubles += (b == c)
		if b + c in ('ab', 'cd', 'pq', 'xy'):
			return False
		b = c
	return vowels >= 3 and doubles > 0

print(sum(map(is_nice, sys.stdin)))
