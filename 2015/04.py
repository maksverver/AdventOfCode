from hashlib import md5
import sys

def solve(key, len):
	i = 1
	while md5(bytes(key + str(i), 'ascii')).hexdigest()[:len] != '0'*len:
		i += 1
	return i

key = sys.stdin.readline().strip()
print(solve(key, 5))  # Part 1
print(solve(key, 6))  # Part 2
