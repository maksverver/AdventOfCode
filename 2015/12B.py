import json
import sys

def calc(a):
	if type(a) is int:
		return int(a)
	if type(a) is list:
		return sum(map(calc, a))
	if type(a) is dict and 'red' not in a.values():
		return sum(map(calc, a.values()))
	return 0

print(calc(json.loads(sys.stdin.read())))
