import sys
	
memo = [0] + 150*[float('inf')]
for size in map(int, sys.stdin):
	memo = [ count if total < size else min(count, memo[total - size] + 1)
	         for (total, count) in enumerate(memo) ]
print memo[150]
