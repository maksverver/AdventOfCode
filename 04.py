import md5
import sys

key = sys.stdin.readline().strip()
i = 1
while md5.new(key + str(i)).hexdigest()[:5] != '00000':
	i += 1
print i  # Part 1
while md5.new(key + str(i)).hexdigest()[:6] != '000000':
	i += 1
print i  # Part 2
