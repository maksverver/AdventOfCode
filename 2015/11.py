import sys

forbidden = 'iol'  # important: neither 'a' nor 'z' are forbidden

def remove_forbidden(s):
	for i in range(len(s)):
		if s[i] in forbidden:
			while s[i] in forbidden:
				s[i] = next_char(s[i])
			for j in range(i + 1, len(s)):
				s[j] = 'a'
			break

def next_char(c):
	assert 'a' <= c < 'z'
	return chr(ord(c) + 1)

def inc(s):
	i = len(s) - 1
	while s[i] == 'z':
		s[i] = 'a'
		i = i - 1
	s[i] = next_char(s[i])
	while s[i] in forbidden:
		s[i] = next_char(s[i])
	return s

def has_straight(s):
	# Must include an increasing triple (e. g. 'xyz')
	for i in range(2, len(s)):
		if ord(s[i - 2]) + 2 == ord(s[i - 1]) + 1 == ord(s[i]):
			break
	else:
		return False
	return True

def has_pairs(s):
	# Must include two different character pairs
	pair = None
	for i in range(1, len(s)):
		if s[i - 1] == s[i]:
			if pair == None:
				pair = s[i]
			elif pair != s[i]:
				break
	else:
		return False
	return True

def valid(s):
	return has_straight(s) and has_pairs(s)

password = list(sys.stdin.readline().strip())
remove_forbidden(password)
while not valid(inc(password)): pass
print ''.join(password)
while not valid(inc(password)): pass
print ''.join(password)
