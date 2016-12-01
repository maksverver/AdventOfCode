import sys
	
memo = [1] + 150*[0]
for size in map(int, sys.stdin):
	memo = [ count if total < size else count + memo[total - size]
	         for (total, count) in enumerate(memo) ]
print memo[150]
