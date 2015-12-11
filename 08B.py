import sys

print sum(2 + line.count('"') + line.count('\\') for line in sys.stdin)
