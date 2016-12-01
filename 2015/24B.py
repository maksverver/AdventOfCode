from itertools import combinations
import sys

product = lambda a: reduce(lambda x, y: x*y, a, 1)

def can_split(weights, w1, w2, w3, pos):
	if pos == len(weights):
		return w1 == w2 == w3 == 0
	w = weights[pos]
	return (
		(w <= w1 and can_split(weights, w1 - w, w2, w3, pos + 1)) or
		(w <= w2 and can_split(weights, w1, w2 - w, w3, pos + 1)) or
		(w <= w3 and can_split(weights, w1, w2, w3 - w, pos + 1)))

def solve(weights):
	assert sum(weights) % 4 == 0
	goal_weight = sum(weights) // 4
	for size in range(1, len(weights)):
		for c in sorted(combinations(weights, size), key=product):
			if sum(c) == goal_weight:
				# assumes weights are unique..
				rest = [ w for w in weights if w not in c ]
				if can_split(rest, goal_weight, goal_weight, goal_weight, 0):
					return product(c)

weights = map(int, sys.stdin)
print solve(weights)
