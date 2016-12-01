def looksay(s):
	t = ''
	i = 0
	while i < len(s):
		j = i + 1
		while j < len(s) and s[j] == s[i]:
			j = j + 1
		t += str(j - i) + s[i]
		i = j
	return t

s = '1113122113'
for _ in range(40):
	s = looksay(s)
print len(s)  # Part 1
for _ in range(10):
	s = looksay(s)
print len(s)  # Part 2
