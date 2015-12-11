import sys

print sum(len(line.strip()) - len(eval(line)) for line in sys.stdin)
