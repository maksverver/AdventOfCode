import sys

def is_nice(word):
	return any(word[i - 2] == word[i] for i in range(2, len(word))) and \
		any(word[i-2:i] in word[0:i-2] for i in range(2, len(word)))

print(sum(map(is_nice, sys.stdin)))
