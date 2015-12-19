from collections import defaultdict
import sys

replacements = defaultdict(list)

def find_all(s, t):
	i = -1
	while True:
		i = s.find(t, i + 1)
		if i < 0: return
		yield i

def calibrate(s):
	ts = set()
	for k, rs in replacements.iteritems():
		for i in find_all(s, k):
			for r in rs:
				t = s[:i] + r + s[i + len(k):]
				ts.add(t)
	return ts

for line in sys.stdin:
	line = line.strip()
	if line == '': break
	s, t = line.split(' => ')
	replacements[s].append(t)
for line in sys.stdin:
	goal = line.strip()
	print len(calibrate(goal))
