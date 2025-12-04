import sys

def inc(a):
	(count, combis) = a
	return (count + 1, combis)

def update(a, b):
	(old_count, old_combis) = a
	(new_count, new_combis) = b
	if old_count < new_count:
		return (old_count, old_combis)
	if new_count < old_count:
		return (new_count, new_combis)
	return (old_count, old_combis + new_combis)

memo = [(0,1)] + 150*[(float('inf'), 0)]
for size in map(int, sys.stdin):
	memo = [ old if total < size else update(old, inc(memo[total - size]))
	         for (total, old) in enumerate(memo) ]
print(memo[150][1])
