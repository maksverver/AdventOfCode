from itertools import combinations
import sys

product = lambda a: reduce(lambda x, y: x*y, a, 1)

def can_split(weights, remaining, pos):
	if remaining == 0:
		return True
	if pos == len(weights):
		return False
	return (
		can_split(weights, remaining - weights[pos], pos + 1) or
		can_split(weights, remaining, pos + 1))

def solve(weights):
	assert sum(weights) % 3 == 0
	goal_weight = sum(weights) // 3
	for size in range(1, len(weights)):
		for c in sorted(combinations(weights, size), key=product):
			if sum(c) == goal_weight:
				# assumes weights are unique..
				rest = [ w for w in weights if w not in c ]
				if can_split(rest, goal_weight, 0):
					return product(c)

weights = map(int, sys.stdin)
print solve(weights)
