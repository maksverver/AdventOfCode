from collections import defaultdict
import sys

ingredients = []
properties = defaultdict(dict)

def evaluate(taken):
	totals = defaultdict(int)
	for (name, amount) in zip(ingredients, taken):
		for prop, score in properties[name].items():
			totals[prop] += score*amount
	if totals['calories'] != 500:
		return 0
	del totals['calories']
	res = 1
	for total in totals.values():
		if total <= 0:
			return 0
		res *= total
	return res

def search(taken, left):
	if len(taken) + 1 == len(properties):
		return evaluate(taken + [left])
	return max(search(taken + [t], left - t) for t in range(0, left + 1))

for line in sys.stdin:
	parts = line.split()
	name = parts[0].rstrip(':')
	ingredients.append(name)
	for i in range(1, len(parts), 2):
		properties[name][parts[i]] = int(parts[i + 1].rstrip(','))

print search([], 100)
